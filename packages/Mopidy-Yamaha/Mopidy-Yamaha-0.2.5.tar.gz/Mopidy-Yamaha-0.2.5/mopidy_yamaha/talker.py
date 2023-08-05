import logging

import urllib2

import pykka

import xmltodict

logger = logging.getLogger(__name__)


class YamahaTalker(pykka.ThreadingActor):
    """
    Independent thread which does the communication with the Yamaha amplifier.

    Since the communication is done in an independent thread, Mopidy won't
    block other requests while sending commands to the receiver.
    """

    _min_volume = -805

    def __init__(self, host, source=None, party_mode=None):
        super(YamahaTalker, self).__init__()

        self.host = host
        self.source = source
        self.party_mode = party_mode
        print "source=%s party_mode=%s" % (source,self.party_mode)

        self._model = None

    def on_start(self):
        self._get_device_model()
        self._set_device_to_known_state()

    def _set_device_to_known_state(self):
        self._power_device_on()
        self._select_input_source()
        self.mute(False)
        self._set_party_mode()

    def _get_device_model(self):
        logger.info('Yamaha amplifier: Get device model from host "%s"',
                    self.host)
        response = self._get('<Config>GetParam</Config>', zone='System')
        self._model = response['Config']['Model_Name']
        logger.info('Yamaha amplifier: Found device model "%s"', self._model)

    def _power_device_on(self):
        self._put('<Power_Control><Power>On</Power></Power_Control>',
                  zone='System')

    def _select_input_source(self):
        if self.source is not None:
            self._put('<Input><Input_Sel>%s</Input_Sel></Input>' % self.source)

    def _set_party_mode(self):
        if self.party_mode is not None:
            mode = 'On' if self.party_mode else 'Off'
            self._put(
                '<Party_Mode><Mode>%s</Mode></Party_Mode>' % mode,
                zone='System')

    def mute(self, mute):
        request = '<Volume><Mute>%s</Mute></Volume>'
        if mute:
            self._put(request % 'On')
        else:
            self._put(request % 'Off')

    def get_volume(self):
        response = self._get('<Basic_Status>GetParam</Basic_Status>')
        volume = int(response['Basic_Status']['Volume']['Lvl']['Val'])
        percentage_volume = (
            -(volume - self._min_volume)
            / float(self._min_volume)
            ) * 100
        logger.info(
            'Yamaha amplifier: Volume is "%d" (%d%%)',
            volume, percentage_volume)
        return percentage_volume

    def set_volume(self, volume):
        db_volume = (
            -volume / 100.0 * self._min_volume
            ) + self._min_volume
        db_volume = int(db_volume - (db_volume % 5))
        logger.debug(
            'Yamaha amplifier: Set volume to "%d" (%d%%)',
            db_volume, volume)
        self._put('''<Volume>
                <Lvl><Val>%d</Val><Exp>1</Exp><Unit>dB</Unit></Lvl>
            </Volume>''' % db_volume)
        return True

    def _put(self, request_xml, zone='Main_Zone'):
        return self._send_command(
            method='PUT', request_xml=request_xml, zone=zone)

    def _get(self, request_xml, zone='Main_Zone'):
        return self._send_command(
            method='GET', request_xml=request_xml, zone=zone)[zone]

    def _send_command(self, method, request_xml, zone):
        zone_xml = (
            '<%(zone)s>%(xml)s</%(zone)s>'
            % {'zone': zone, 'xml': request_xml}
            )
        data = '<YAMAHA_AV cmd="%s">%s</YAMAHA_AV>' % (method, zone_xml)
        logger.debug('Yamaha amplifier: Send command "%s"' % data)
        request = urllib2.Request(
            url='http://%s/YamahaRemoteControl/ctrl' % self.host,
            data=data,
            headers={'Content-Type': 'text/xml'})
        connection = urllib2.urlopen(request)
        response = connection.read()
        connection.close()
        return xmltodict.parse(response)['YAMAHA_AV']

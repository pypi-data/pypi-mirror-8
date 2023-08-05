from .common import *
from av.codec import Codec, Encoder, Decoder


class TestCodecs(TestCase):

    def test_codec_mpeg4(self):
        for cls in (Encoder, Decoder):
            c = cls('mpeg4')
            self.assertEqual(c.name, 'mpeg4')
            self.assertEqual(c.long_name, 'MPEG-4 part 2')
            self.assertEqual(c.type, 'video')
            self.assertEqual(c.id, 13)

            formats = c.video_formats
            self.assertTrue(formats)
            self.assertTrue(any(f.name == 'yuv420p' for f in formats))

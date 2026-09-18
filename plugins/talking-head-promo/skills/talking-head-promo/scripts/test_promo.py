import unittest, tempfile, pathlib, argparse
from unittest.mock import patch
import promo

class WorkflowTests(unittest.TestCase):
    def test_quota_exhausted_blocks(self):
        with self.assertRaisesRegex(RuntimeError,'不足'): promo.quota_decision(dict(tier='free',max_credit_limit_extension=0,character_count=10000,character_limit=10000),140)
    def test_quota_overage_enabled_blocks(self):
        with self.assertRaisesRegex(RuntimeError,'超额计费'): promo.quota_decision(dict(tier='free',max_credit_limit_extension='unlimited',character_count=0,character_limit=10000),140)
    def test_quota_unknown_and_paid_block(self):
        for data in ({},dict(tier='creator'),dict(tier='free',max_credit_limit_extension=0)):
            with self.assertRaises(RuntimeError): promo.quota_decision(data,140)
    def test_quota_free_with_reserve(self):
        self.assertEqual(promo.quota_decision(dict(tier='free',max_credit_limit_extension=0,character_count=0,character_limit=10000),140)['safety_reserve'],4500)
    def test_finish_compiles_actual_caption_clips(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)
            p=dict(width=1280,height=720,fps=30,duration=3,scenes=[dict(id='test',pattern='title',start=0,end=3,title='测试')])
            promo.save(root/'plan.json',p)
            promo.save(root/'captions.json',[dict(start=.5,end=2,text='口播字幕')])
            promo.finish(argparse.Namespace(project=str(root),render=False))
            html=(root/'composition'/'index.html').read_text(encoding='utf-8')
            self.assertIn('口播字幕',html)
            self.assertIn('id="caption-0" data-start="0.5"',html)
            self.assertEqual(promo.load(root/'composition'/'plan.json')['captions'][0]['end'],2)
    def test_chinese_and_english(self):
        words=[dict(type='word',start=0,end=.4,text='你好'),dict(type='word',start=.4,end=.9,text='。'),dict(type='word',start=1,end=1.2,text='Hello'),dict(type='spacing',start=1.2,end=1.2,text=' '),dict(type='word',start=1.2,end=1.8,text='world!')]
        c=promo.captions(words)
        self.assertEqual([x['text'] for x in c],['你好。','Hello world!'])
        self.assertEqual(c[1]['end'],1.8)
    def test_bad_timestamps(self):
        with self.assertRaises(RuntimeError): promo.captions([dict(type='word',start=2,end=1,text='x')])
    def test_readability_split(self):
        w=[dict(type='word',start=i,end=i+.5,text='测试') for i in range(12)]
        self.assertTrue(all(len(x['text'])<=6 for x in promo.captions(w,max_chars=6)))
    def test_srt_and_saved_cues(self):
        with tempfile.TemporaryDirectory() as d:
            work=pathlib.Path(d)
            promo.outputs(work,dict(words=[dict(type='word',start=1.25,end=2.5,text='字幕')]))
            self.assertIn('00:00:01,250 --> 00:00:02,500',(work/'subtitles.srt').read_text(encoding='utf-8'))
    def test_cache_never_calls_api(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d);src=root/'voice.mp4';src.write_bytes(b'fixture');work=root/'work';work.mkdir()
            promo.save(work/'transcript.json',dict(words=[dict(type='word',start=0,end=1,text='cache')]))
            args=argparse.Namespace(video=str(src),project=str(work),model='scribe_v2',retry_upload=False,allow_upload=False)
            with patch.object(promo,'doctor',return_value=True),patch.object(promo,'request_transcript') as api:
                promo.prepare(args);api.assert_not_called()
    def test_uncertain_stops_duplicate_billing(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d);src=root/'voice.mp4';src.write_bytes(b'fixture');work=root/'work';work.mkdir()
            promo.save(work/'workflow.json',dict(source_sha256=promo.hashlib.sha256(b'fixture').hexdigest(),model='scribe_v2',stage='uploading'))
            args=argparse.Namespace(video=str(src),project=str(work),model='scribe_v2',retry_upload=False,allow_upload=True)
            with patch.object(promo,'doctor',return_value=True),patch.object(promo,'request_transcript') as api:
                with self.assertRaisesRegex(RuntimeError,'上次请求'): promo.prepare(args)
                api.assert_not_called()

if __name__=='__main__': unittest.main()

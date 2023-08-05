# -*- coding: utf-8 -*-
from __future__ import with_statement

import collections
import io
import json
import os
import os.path
import re
import shutil
import tempfile
import unittest

from six import PY3, StringIO, b, text_type
from werkzeug.test import Client
from werkzeug.wrappers import Response

import sass
import sassc
from sassutils.builder import Manifest, build_directory
from sassutils.wsgi import SassMiddleware


A_EXPECTED_CSS = '''\
body {
  background-color: green; }
  body a {
    color: blue; }
'''

A_EXPECTED_CSS_WITH_MAP = '''\
body {
  background-color: green; }
  body a {
    color: blue; }

/*# sourceMappingURL=a.scss.css.map */'''

A_EXPECTED_MAP = {
    'version': 3,
    'file': '',
    'sources': ['test/a.scss'],
    'names': [],
    'mappings': 'AAKA;EAHE,kBAAkB;EAIpB,KAAK;IAED,OAAO'
}

B_EXPECTED_CSS = '''\
b i {
  font-size: 20px; }
'''

C_EXPECTED_CSS = '''\
body {
  background-color: green; }
  body a {
    color: blue; }

h1 a {
  color: green; }
'''

D_EXPECTED_CSS = '''\
body {
  background-color: green; }
  body a {
    font: '나눔고딕', sans-serif; }
'''

SUBDIR_RECUR_EXPECTED_CSS = '''\
body p {
  color: blue; }
'''

utf8_if_py3 = {'encoding': 'utf-8'} if PY3 else {}


class SassTestCase(unittest.TestCase):

    def test_version(self):
        assert re.match(r'^\d+\.\d+\.\d+$', sass.__version__)

    def test_output_styles(self):
        if hasattr(collections, 'Mapping'):
            assert isinstance(sass.OUTPUT_STYLES, collections.Mapping)
        assert 'nested' in sass.OUTPUT_STYLES

    def test_and_join(self):
        self.assertEqual(
            'Korea, Japan, China, and Taiwan',
            sass.and_join(['Korea', 'Japan', 'China', 'Taiwan'])
        )
        self.assertEqual(
            'Korea, and Japan',
            sass.and_join(['Korea', 'Japan'])
        )
        self.assertEqual('Korea', sass.and_join(['Korea']))
        self.assertEqual('', sass.and_join([]))


class CompileTestCase(unittest.TestCase):

    def test_compile_required_arguments(self):
        self.assertRaises(TypeError, sass.compile)


    def test_compile_takes_only_keywords(self):
        self.assertRaises(TypeError, sass.compile, 'a { color: blue; }')

    def test_compile_exclusive_arguments(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', filename='test/a.scss')
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', dirname='test/')
        self.assertRaises(TypeError,  sass.compile,
                          filename='test/a.scss', dirname='test/')

    def test_compile_invalid_output_style(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }',
                          output_style=['compact'])
        self.assertRaises(TypeError,  sass.compile,
                          string='a { color: blue; }', output_style=123j)
        self.assertRaises(ValueError,  sass.compile,
                          string='a { color: blue; }', output_style='invalid')

    def test_compile_invalid_source_comments(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }',
                          source_comments=['line_numbers'])
        self.assertRaises(TypeError,  sass.compile,
                          string='a { color: blue; }', source_comments=123j)
        self.assertRaises(ValueError,  sass.compile,
                          string='a { color: blue; }',
                          source_comments='invalid')
        # map requires source_map_filename
        self.assertRaises(ValueError,  sass.compile,
                          string='a { color: blue; }',
                          source_comments='map')

    def test_compile_invalid_image_path(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', image_path=[])
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', image_path=123)

    def test_compile_string(self):
        actual = sass.compile(string='a { b { color: blue; } }')
        assert actual == 'a b {\n  color: blue; }\n'
        commented = sass.compile(string='''a {
            b { color: blue; }
            color: red;
        }''', source_comments='line_numbers')
        assert commented == '''/* line 1, source string */
a {
  color: red; }
  /* line 2, source string */
  a b {
    color: blue; }
'''
        actual = sass.compile(string=u'a { color: blue; } /* 유니코드 */')
        self.assertEqual(
            u'''a {
  color: blue; }

/* 유니코드 */''',
            actual
        )
        self.assertRaises(sass.CompileError, sass.compile,
                          string='a { b { color: blue; }')
        # sass.CompileError should be a subtype of ValueError
        self.assertRaises(ValueError, sass.compile,
                          string='a { b { color: blue; }')
        self.assertRaises(TypeError, sass.compile, string=1234)
        self.assertRaises(TypeError, sass.compile, string=[])
        # source maps are available only when the input is a filename
        self.assertRaises(sass.CompileError, sass.compile,
                          string='a { b { color: blue; }',
                          source_comments='map')

    def test_compile_filename(self):
        actual = sass.compile(filename='test/a.scss')
        assert actual == A_EXPECTED_CSS
        actual = sass.compile(filename='test/c.scss')
        assert actual == C_EXPECTED_CSS
        actual = sass.compile(filename='test/d.scss')
        if text_type is str:
            self.assertEqual(D_EXPECTED_CSS, actual)
        else:
            self.assertEqual(D_EXPECTED_CSS.decode('utf-8'), actual)
        self.assertRaises(IOError, sass.compile,
                          filename='test/not-exist.sass')
        self.assertRaises(TypeError, sass.compile, filename=1234)
        self.assertRaises(TypeError, sass.compile, filename=[])

    def test_compile_source_map(self):
        actual, source_map = sass.compile(
            filename='test/a.scss',
            source_comments='map',
            source_map_filename='a.scss.css.map'
        )
        self.assertEqual(A_EXPECTED_CSS_WITH_MAP, actual)
        self.assertEqual(
            A_EXPECTED_MAP,
            json.loads(source_map)
        )

    def test_regression_issue_2(self):
        actual = sass.compile(string='''
            @media (min-width: 980px) {
                a {
                    color: red;
                }
            }
        ''')
        normalized = re.sub(r'\s+', '', actual)
        assert normalized == '@media(min-width:980px){a{color:red;}}'

    def test_regression_issue_11(self):
        actual = sass.compile(string='''
            $foo: 3;
            @media (max-width: $foo) {
                body { color: black; }
            }
        ''')
        normalized = re.sub(r'\s+', '', actual)
        assert normalized == '@media(max-width:3){body{color:black;}}'


class BuilderTestCase(unittest.TestCase):

    def test_builder_build_directory(self):
        temp_path = tempfile.mkdtemp()
        sass_path = os.path.join(temp_path, 'sass')
        css_path = os.path.join(temp_path, 'css')
        shutil.copytree('test', sass_path)
        result_files = build_directory(sass_path, css_path)
        assert len(result_files) == 5
        assert result_files['a.scss'] == 'a.scss.css'
        with open(os.path.join(css_path, 'a.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        assert css == A_EXPECTED_CSS
        assert result_files['b.scss'] == 'b.scss.css'
        with open(os.path.join(css_path, 'b.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        assert css == B_EXPECTED_CSS
        assert result_files['c.scss'] == 'c.scss.css'
        with open(os.path.join(css_path, 'c.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        assert css == C_EXPECTED_CSS
        assert result_files['d.scss'] == 'd.scss.css'
        with open(os.path.join(css_path, 'd.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        self.assertEqual(D_EXPECTED_CSS, css)
        assert (result_files[os.path.join('subdir', 'recur.scss')] ==
                os.path.join('subdir', 'recur.scss.css'))
        with open(os.path.join(css_path, 'subdir', 'recur.scss.css'),
                  **utf8_if_py3) as f:
            css = f.read()
        self.assertEqual(SUBDIR_RECUR_EXPECTED_CSS, css)
        shutil.rmtree(temp_path)


class ManifestTestCase(unittest.TestCase):

    def test_normalize_manifests(self):
        manifests = Manifest.normalize_manifests({
            'package': 'sass/path',
            'package.name': ('sass/path', 'css/path'),
            'package.name2': Manifest('sass/path', 'css/path')
        })
        assert len(manifests) == 3
        assert isinstance(manifests['package'], Manifest)
        assert manifests['package'].sass_path == 'sass/path'
        assert manifests['package'].css_path == 'sass/path'
        assert isinstance(manifests['package.name'], Manifest)
        assert manifests['package.name'].sass_path == 'sass/path'
        assert manifests['package.name'].css_path == 'css/path'
        assert isinstance(manifests['package.name2'], Manifest)
        assert manifests['package.name2'].sass_path == 'sass/path'
        assert manifests['package.name2'].css_path == 'css/path'

    def test_build_one(self):
        d = tempfile.mkdtemp()
        src_path = os.path.join(d, 'test')
        if os.sep != '/' and os.altsep:
            normalize = lambda p: os.path.abspath(
                os.path.normpath(os.path.join(src_path, p))
            ).replace(os.sep, os.altsep)
        else:
            normalize = lambda p: p
        try:
            shutil.copytree('test', src_path)
            m = Manifest(sass_path='test', css_path='css')
            m.build_one(d, 'a.scss')
            with open(os.path.join(d, 'css', 'a.scss.css')) as f:
                self.assertEqual(A_EXPECTED_CSS, f.read())
            m.build_one(d, 'b.scss', source_map=True)
            with open(os.path.join(d, 'css', 'b.scss.css'),
                      **utf8_if_py3) as f:
                self.assertEqual(
                    B_EXPECTED_CSS +
                    '\n/*# sourceMappingURL=b.scss.css.map */',
                    f.read()
                )
            self.assert_json_file(
                {
                    'version': 3,
                    'file': '',
                    'sources': [normalize('../test/b.scss')],
                    'names': [],
                    'mappings': 'AAAA,EAAE;EAEE,WAAW'
                },
                os.path.join(d, 'css', 'b.scss.css.map')
            )
            m.build_one(d, 'd.scss', source_map=True)
            with open(os.path.join(d, 'css', 'd.scss.css'),
                      **utf8_if_py3) as f:
                self.assertEqual(
                    D_EXPECTED_CSS +
                    '\n/*# sourceMappingURL=d.scss.css.map */',
                    f.read()
                )
            self.assert_json_file(
                {
                    'version': 3,
                    'file': '',
                    'sources': [normalize('../test/d.scss')],
                    'names': [],
                    'mappings': 'AAKA;EAHE,kBAAkB;EAIpB,KAAK;IAED,MAAM'
                },
                os.path.join(d, 'css', 'd.scss.css.map')
            )
        finally:
            shutil.rmtree(d)

    def assert_json_file(self, expected, filename):
        with open(filename) as f:
            try:
                tree = json.load(f)
            except ValueError as e:
                f.seek(0)
                msg = '{0!s}\n\n{1}:\n\n{2}'.format(e, filename, f.read())
                raise ValueError(msg)
        self.assertEqual(expected, tree)


class WsgiTestCase(unittest.TestCase):

    @staticmethod
    def sample_wsgi_app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return environ['PATH_INFO'],

    def test_wsgi_sass_middleware(self):
        css_dir = tempfile.mkdtemp()
        try:
            app = SassMiddleware(self.sample_wsgi_app, {
                __name__: ('test', css_dir, '/static')
            })
            client = Client(app, Response)
            r = client.get('/asdf')
            self.assertEqual(200, r.status_code)
            self.assert_bytes_equal(b'/asdf', r.data)
            self.assertEqual('text/plain', r.mimetype)
            r = client.get('/static/a.scss.css')
            self.assertEqual(200, r.status_code)
            self.assert_bytes_equal(b(A_EXPECTED_CSS_WITH_MAP), r.data)
            self.assertEqual('text/css', r.mimetype)
            r = client.get('/static/not-exists.sass.css')
            self.assertEqual(200, r.status_code)
            self.assert_bytes_equal(b'/static/not-exists.sass.css', r.data)
            self.assertEqual('text/plain', r.mimetype)
        finally:
            shutil.rmtree(css_dir)

    def assert_bytes_equal(self, expected, actual, *args):
        self.assertEqual(expected.replace(b'\r\n', b'\n'),
                         actual.replace(b'\r\n', b'\n'),
                         *args)


class SasscTestCase(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()
        self.err = StringIO()

    def test_no_args(self):
        exit_code = sassc.main(['sassc', ], self.out, self.err)
        self.assertEqual(2, exit_code)
        err = self.err.getvalue()
        assert err.strip().endswith('error: too few arguments'), \
               'actual error message is: ' + repr(err)
        self.assertEqual('', self.out.getvalue())

    def test_three_args(self):
        exit_code = sassc.main(
            ['sassc', 'a.scss', 'b.scss', 'c.scss'],
            self.out, self.err
        )
        self.assertEqual(2, exit_code)
        err = self.err.getvalue()
        assert err.strip().endswith('error: too many arguments'), \
               'actual error message is: ' + repr(err)
        self.assertEqual('', self.out.getvalue())

    def test_sassc_stdout(self):
        exit_code = sassc.main(['sassc', 'test/a.scss'], self.out, self.err)
        self.assertEqual(0, exit_code)
        self.assertEqual('', self.err.getvalue())
        self.assertEqual(A_EXPECTED_CSS.strip(), self.out.getvalue().strip())

    def test_sassc_output(self):
        fd, tmp = tempfile.mkstemp('.css')
        try:
            os.close(fd)
            exit_code = sassc.main(['sassc', 'test/a.scss', tmp],
                                   self.out, self.err)
            self.assertEqual(0, exit_code)
            self.assertEqual('', self.err.getvalue())
            self.assertEqual('', self.out.getvalue())
            with open(tmp) as f:
                self.assertEqual(A_EXPECTED_CSS.strip(), f.read().strip())
        finally:
            os.remove(tmp)

    def test_sassc_output_unicode(self):
        fd, tmp = tempfile.mkstemp('.css')
        try:
            os.close(fd)
            exit_code = sassc.main(['sassc', 'test/d.scss', tmp],
                                   self.out, self.err)
            self.assertEqual(0, exit_code)
            self.assertEqual('', self.err.getvalue())
            self.assertEqual('', self.out.getvalue())
            with open(tmp, **utf8_if_py3) as f:
                self.assertEqual(
                    D_EXPECTED_CSS.strip(),
                    f.read().strip()
                )
        finally:
            os.remove(tmp)

    def test_sassc_source_map_without_css_filename(self):
        exit_code = sassc.main(['sassc', '-m', 'a.scss'], self.out, self.err)
        self.assertEqual(2, exit_code)
        err = self.err.getvalue()
        assert err.strip().endswith('error: -m/-g/--sourcemap requires '
                                    'the second argument, the output css '
                                    'filename.'), \
               'actual error message is: ' + repr(err)
        self.assertEqual('', self.out.getvalue())

    def test_sassc_sourcemap(self):
        fd, tmp = tempfile.mkstemp('.css')
        try:
            os.close(fd)
            exit_code = sassc.main(['sassc', '-m', 'test/a.scss', tmp],
                                   self.out, self.err)
            self.assertEqual(0, exit_code)
            self.assertEqual('', self.err.getvalue())
            self.assertEqual('', self.out.getvalue())
            with open(tmp) as f:
                self.assertEqual(
                    A_EXPECTED_CSS + '\n/*# sourceMappingURL=' + 
                    os.path.basename(tmp) + '.map */',
                    f.read().strip()
                )
            with open(tmp + '.map') as f:
                self.assertEqual(
                    dict(A_EXPECTED_MAP, sources=None),
                    dict(json.load(f), sources=None)
                )
        finally:
            os.remove(tmp)


test_cases = [
    SassTestCase,
    CompileTestCase,
    BuilderTestCase,
    ManifestTestCase,
    WsgiTestCase,
    SasscTestCase
]
loader = unittest.defaultTestLoader
suite = unittest.TestSuite()
for test_case in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(test_case))

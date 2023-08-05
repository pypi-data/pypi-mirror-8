'''
Copyright 2012-2014 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


from qualitylib.formatting import DotFormatter
from unittests.formatting import fake_report, fake_domain
import unittest


class DotFormatterTest(unittest.TestCase):  
    # pylint: disable=too-many-public-methods
    ''' Unit test for the GraphViz dot report formatter class. '''
    def setUp(self):  # pylint: disable=invalid-name
        self.__formatter = DotFormatter()

    def test_prefix(self):
        ''' Test that the formatter returns the correct prefix. '''
        self.assertEqual('digraph { ranksep="2.5"; concentrate="true";', 
                         self.__formatter.prefix(None))

    def test_body_empty_report(self):
        ''' Test that the formatter returns '''
        self.assertEqual('', self.__formatter.body(fake_report.Report()))

    def test_body_one_product(self):
        ''' Test that the body returns a graph with one product. '''
        self.assertEqual('  subgraph "cluster-Fake Product" {\n'
                         '    label="Fake Product"; fillcolor="lightgrey"; '
                         'style="filled"\n'
                         '    "Fake Product:1" [label="1" style="filled" '
                         'fillcolor="green" URL="index.html#section_FP" '
                         'target="_top"];\n  };', 
                         self.__formatter.body(fake_report.Report( \
                                               [fake_domain.Product()])))

    def test_body_one_product_dependency(self):
        ''' Test that the body returns a graph with one product dependency. '''
        report = fake_report.Report([fake_domain.Product(True)])
        self.assertEqual('  subgraph "cluster-Fake Product" {\n'
                         '    label="Fake Product"; fillcolor="lightgrey"; '
                         'style="filled"\n'
                         '    "Fake Product:1" [label="1" style="filled" '
                         'fillcolor="green" URL="index.html#section_FP" '
                         'target="_top"];\n  };\n'
                         '  "Fake Product:1" -> "Fake Dependency:1";',
                         self.__formatter.body(report))

    def test_postfix(self):
        ''' Test that the formatter returns the correct postfix. ''' 
        self.assertEqual('}\n', self.__formatter.postfix())

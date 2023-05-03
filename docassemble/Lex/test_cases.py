import unittest
from docassemble.base.util import as_datetime
from random import choice
from .cases36 import SCCase, SCJurisdiction, the_states

class TestJurisdiction(unittest.TestCase):

    def test_doc_header(self):
        for state in the_states():
          case = SCCase()
          case.juris.jurisdiction.name.text = "state"
          case.juris.state.name.text = state
          case.juris.county.name.text = choice(case.juris.trial_court_unit_keys())
          if case.juris.trial_court_has_multiple_unit_types():
            if type(case.juris.trial_court_unit_dictionary()[case.juris.county.name.text]) == list:
              case.juris.district.name.trxt = choice(case.juris.trial_court_unit_dictionary()[case.juris.county.name.text])
          if case.juris.trial_court_has_divisions():
            case.juris.division.name.text = choice(case.juris.trial_court_divisions())
          if case.juris.case_no_in_header():
            case.docket_number = "555555"
          self.assertIsNotNone(case.doc_header())

    

if __name__ == '__main__':
    unittest.main()
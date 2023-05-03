import unittest
from .fixtures import fixture_for_results_of_ocrd_text_including_rfp, fixture_for_results_of_ocrd_text_including_rfa, fixture_for_results_of_ocrd_text_including_rog

class TestLegete(unittest.TestCase):

  def test_quaero_rrfps(self):
    result = quaero_rrfps(fixture_for_results_of_ocrd_text_including_rfp)
    rfp = [
      [
        "A copy of Plaintiffs proof of\nautomobile/motorcycle liability insurance in force at the time of the incident.", 
        0
      ], 
      [
        "The name, address, and telephone numbers for\nall persons who are claimed to have seen the incident, or who arrived afterwards.", 
        0
      ], 
      [
        "A copy of any and all statements, written,\nrecorded or otherwise, taken regarding this incident that were made by: Defendant, all\nwitnesses, law enforcement individuals or emergency response personnel present at the\nscene of the incident.", 
        0
      ]
    ]
    self.assertEqual(result, rfp)
  def test_quaero_rfas(self):
    result = quaero_rrfps(fixture_for_results_of_ocrd_text_including_rfa)
    rfa =   [
      [
        "Admit that plaintiff was injured jumping from a railing on the\nsubject pontoon boat.", 
        2
      ], 
      [
        "Admit that plaintiff was instructed \u201cPlease, do not jump off\nrailings or seats\u201d prior to the incident.", 
        2
      ], 
      [
        "Admit that plaintiff had consumed alcohol prior to the incident", 
        2
      ], 
      [
        "Admit that plaintiff was intoxicated at the time of the incident.\n-", 
        2
      ], 
      [
        "Admit that the plaintiff was injured, in whole or in part, as the\nresult of his own negligence.", 
        2
      ], 
      [
        "811 SW Naito Parkway, Suite 500\nPortland, OR 97204\n(503) 223-4131 / (503) 223-1346 fax\ngkeating @schulte-law.com\nAttorney for Defendant\n  CERTIFICATE OF SERVICE\n\nI hereby certify that I served a true and correct copy of the foregoing DEFENDANT\u2019S\nFIRST REQUEST FOR ADMISSIONS TO PLAINTIFF on the date indicated below and to\nthe party/attorney(s) indicated below:\n\nXx courtesy mail with postage prepaid, deposited in the US mail at Portland, Oregon;\nI further certify that said copy was placed in a sealed envelope delivered to attorneys at the\naddresses listed below.\n\n[] OJD Efiling System (File & Serve) (i.e., \u201cElectronic service\u201d means the electronic\ntransmission of a notice of filing by the electronic filing system to the electronic mail (email)\naddress of a party who has consented to electronic service under UTCR", 
        3
      ]
    ]
    self.assertEqual(result, rfa)
  def test_quaero_rogs(self):
    result = quaero_rrfps(fixture_for_results_of_ocrd_text_including_rog)
    rog = [
      [
        "State the names and addresses and phone numbers of all\npersons who were assisting Plaintiff in the unloading of the JELD-WEN products on May 3,\n2018 just prior to or at the time of the incident.", 
        1
      ], 
      [
        "Describe in detail the manner in which Plaintiff\ncomplied with 49 CFR section 392.9 and 393.100 to 393.136 on April 29, 2018 to May 3, 2018\nwith respect to the JELD-WEN products in the dry van trailer Plaintiff was to deliver.", 
        1
      ], 
      [
        "Please set forth all facts indicating or evidencing that the\ndry van trailer that Plaintiff was driving was sealed as alleged in paragraph 10 of Plaintiff\nAmended Complaint.", 
        1
      ], 
      [
        "State the names and addresses and phone numbers of all\npersons who ordered or prohibited Plaintiff from opening the dry van trailer on April 29, 2018\nprior to commencing the delivery.", 
        1
      ]
    ]
    self.assertEqual(result, rog)

if __name__ == '__main__':
    from docassemble.webapp.server import TestContext
    with TestContext('docassemble.nex'):
        from .legeteme1 import quaero_rrfps
        unittest.main()
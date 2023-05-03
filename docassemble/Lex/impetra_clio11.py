from docassemble.base.util import DAOAuth, DAWeb, DAWebError, log, DAFile, DAObject, DADict, DASet, DAList, ocr_file_in_background
from docassemble.base.functions import defined
import math
import requests
import collections.abc as abc
import re
import json
from pydantic import BaseModel

__all__ = ['ClioAuth', 'ClioZed', 'ClioLed', 'without_keys', 'AliensInvade', 'str_to_json', 'parse_aliens', 'parse_alienids', 'prae_aliens', 'balien', 'body_snatch_lawyer', 'body_snatch_lawfirm', 'body_snatch_party', 'alien_id', 'hatch_case']

def hatch_case(alien_matter, case):
  case.id = alien_matter['id']
  case.doi_vid = alien_matter['doi_vid']
  case.doi_id = alien_matter['doi_id']
  case.number_vid = alien_matter['number_vid']
  case.number_id = alien_matter['number_id']
  case.juris.jurisdiction_vid = alien_matter['jurisdiction_vid']
  case.juris.jurisdiction_id = alien_matter['jurisdiction_id']
  case.juris.division_vid = alien_matter['division_vid']
  case.juris.division_id = alien_matter['division_id']
  case.juris.district_vid = alien_matter['district_vid']
  case.juris.county_id = alien_matter['county_id']
  case.juris.county_vid = alien_matter['county_vid']
  case.juris.state_vid = alien_matter['state_vid']
  case.juris.state_id = alien_matter['state_id']
  case.claims_id = alien_matter['claims_id']
  case.claims_vid = alien_matter['claims_vid']
  if alien_matter['jurisdiction'] is not None and alien_matter['jurisdiction'] !='':
    case.juris.jurisdiction.name.text = alien_matter['jurisdiction'] 
  if alien_matter['district'] is not None and alien_matter['district'] !='':
    case.juris.district.name.text = alien_matter['district'] 
  if alien_matter['county'] is not None and alien_matter['county'] !='':
    case.juris.county.name.text  = alien_matter['county'] 
  if alien_matter['state'] is not None and alien_matter['state'] !='':
    case.juris.state.name.text  = alien_matter['state'] 
  if alien_matter['division'] is not None and alien_matter['division'] !='':
    case.juris.jurisdiction.name.text  = alien_matter['division'] 
  if alien_matter['doi'] is not None and alien_matter['doi'] !='':
    case.doi = alien_matter['doi'] 
  if alien_matter['docket_number'] is not None and alien_matter['docket_number'] !='':
    case.docket_number = alien_matter['docket_number'] 
  if alien_matter['claims'] is not None and alien_matter['claims'] !='':
    case.claims = alien_matter['claims']
  case.relationships = alien_matter['relationships']
  
def alien_id(xxx, ix):
        if hasattr(ix, 'id'):
          xxx.id = ix.id
        xxx.gender_vid = ix.gender_vid
        xxx.is_party_vid = ix.is_party_vid
        xxx.is_lawyer_vid = ix.is_lawyer_vid
        xxx.is_lawfirm_vid = ix.is_lawfirm_vid
        xxx.name.caption_type_vid = ix.name.caption_type_vid
        xxx.caption_text_vid = ix.caption_text_vid
        xxx.party_type_vid = ix.party_type_vid
        xxx.bar_number_vid = ix.bar_number_vid
        xxx.state_bar_vid = ix.state_bar_vid
        xxx.dba_vid = ix.dba_vid
        xxx.trust_vid = ix.trust_vid
        
        
def body_snatch_lawyer(xxx, ix):
            alien_id(xxx, ix)
            if hasattr(ix, 'relationship_id'):
              xxx.relationship_id = ix.relationship_id
            xxx.name.first = ix.name.first
            if ix.name.middle is not None:
              xxx.name.middle = ix.name.middle
            if hasattr(ix, 'email') and ix.email is not None:
              xxx.email = ix.email
              xxx.email_id = ix.email_id
            xxx.name.last = ix.name.last
            if hasattr(ix, 'gender') and ix.gender is not None:
              xxx.gender = ix.gender
            xxx.is_party = False
            xxx.is_lawyer = True
            xxx.is_lawfirm = False
            if hasattr(ix, 'bar_number') and ix.bar_number is not None:
              xxx.bar_number = ix.bar_number
            if hasattr(ix, 'state_bar') and ix.state_bar is not None:
              xxx.state_bar = ix.state_bar
            if hasattr(ix, 'phone') and ix.phone is not None:
              xxx.phone = ix.phone
            xxx.firm = ix.firm
            if hasattr(ix.firm.name, 'text') and ix.firm.name is not None:
              xxx.firm.name.text = ix.firm.name.text
              xxx.firm.id = ix.firm.id
              if hasattr(ix.firm, 'address') and ix.firm.address is not None:
                if ix.firm.address.address is not None and ix.firm.address.address !='':
                  xxx.firm.address.address = ix.firm.address.address
                if ix.firm.address.city is not None and ix.firm.address.city !='':
                  xxx.firm.address.city = ix.firm.address.city
                if ix.firm.address.state is not None and ix.firm.address.state !='':
                  xxx.firm.address.state = ix.firm.address.state
                if ix.firm.address.zip is not None and ix.firm.address.zip !='':
                  xxx.firm.address.zip = ix.firm.address.zip
                xxx.firm.address.unit = None
              xxx.address_id = ix.firm.address.id
            xxx.clio_type = 'Person'
  
def body_snatch_lawfirm(xxx, ix):
            alien_id(xxx, ix)
            if hasattr(ix, 'relationship_id'):
              xxx.relationship_id = ix.relationship_id
            xxx.name.text = ix.name.text
            xxx.is_party = False
            xxx.is_lawyer = False
            xxx.is_lawfirm = True
            #if ix.address is not None:
              #if not defined('xxx.address.address') and ix.address.address is not None and ix.address.address != '':
                #xxx.address.address = ix.address.address
              #if not defined('xxx.address.city') and ix.address.city is not None and ix.address.city != '':
                #xxx.address.city = ix.address.city
              #if not defined('xxx.address.state') and ix.address.state is not None and ix.address.state != '':
                #xxx.address.state = ix.address.state
              #if not defined('xxx.address.zip') and ix.address.zip is not None and ix.address.zip != '':
                #xxx.address.zip = ix.address.zip
              #if not defined('xxx.address.id') and ix.address.id is not None and ix.address.id != '':
                #xxx.address.id = ix.address.id
            xxx.clio_type = 'Company'
  
def body_snatch_party(xxx, ix):
          if hasattr(ix, 'relationship_id'):
            xxx.relationship_id = ix.relationship_id
          if ix.clio_type is not None and ix.clio_type == 'Person':
            if ix.gender is not None and ix.gender != '':
              if ix.gender in ('male', 'female', 'other'):
                xxx.gender = ix.gender
            xxx.name.first = ix.name.first
            if ix.name.middle is not None:
              xxx.name.middle = ix.name.middle
            else: 
              xxx.name.middle = ''
            xxx.name.last = ix.name.last
          else:
            xxx.name.text = ix.name.text
          xxx.is_client = ix.is_client
          xxx.is_party = True
          xxx.is_lawfirm = False
          xxx.is_lawyer = False
          xxx.clio_type = ix.clio_type
          xxx.id = ix.id
          if ix.party_type is not None and ix.party_type != '':
            xxx.party_type = ix.party_type
          if ix.name.caption_type is not None and ix.name.caption_type != '':
            xxx.name.caption_type = ix.name.caption_type
          if ix.caption_text is not None and ix.caption_text != '':
            xxx.caption_text = ix.caption_text
          if ix.dba is not None and ix.dba != '':
            xxx.dba = ix.dba
          if ix.trust is not None and ix.trust != '':
            xxx.trust = ix.trust
          alien_id(xxx, ix)

def parse_alienids(data):
          contactids = {}
          matterids = {}
          allfields = []
          allfields.clear()
          for xxx in data:
            if xxx['parent_type'] == "Contact":
              contactids[str(xxx['name'])] = xxx['id']
              allfields.append(str(xxx['name']))
            else:
              matterids[str(xxx['name'])] = xxx['id']
              allfields.append(str(xxx['name']))
          return (matterids, contactids, allfields)
        
def parse_aliens(data, case):
          throughput = []
          throughput.clear()
          for xxx in data:
            output = {}
            if xxx['relationship'] is not None:
              relationship = xxx['relationship']
              output['relationship_id'] = relationship['id'] 

            output['id'] = xxx['id'] 
            output['name'] = {}
            name = output['name']
            if xxx['type'] == 'Company':
              name['text'] = xxx['name']
            else:
              name['first'] = xxx['first_name'] 
              name['middle'] = xxx['middle_name'] 
              name['last'] = xxx['last_name'] 
              output['company'] = xxx['company']
            if xxx['primary_address'] is not None:
              output['address'] = {}
              yy = xxx['primary_address'] 
              zz = output['address']
              zz['address'] = yy['street']
              zz['city'] = yy['city']
              zz['state'] = yy['province']
              zz['zip'] = yy['postal_code']
            else:
              output['address'] = None
            output['is_client'] = xxx['is_client'] 
            output['email'] = xxx['primary_email_address'] 
            output['phone'] = xxx['primary_phone_number'] 
            customs = xxx['custom_field_values']
            cust = []
            for q in customs:
              output[str(q['field_name'])] = q['value']
              output[str(q['field_name'] + '_vid')] = q['id']
              output[str(q['field_name'] + '_id')] = case.contact_ids_dict[str(q['field_name'])]
              cust.append(q['field_name'])
            if output['is_lawyer'] is not None and output['is_lawyer'] == True:
              if xxx['company'] is not None:
                output['firm'] = {}
                company = xxx['company']
                firm = output['firm']
                firm['name'] = {}
                firmname = firm['name']
                firmname['text'] = company['name']
                output['phone'] = company['primary_phone_number']
                firm['id'] = company['id']
              else: 
                output['firm'] = None
            for item in case.clio_contact_customs:
              if item not in cust:
                output[str(item)] = None
                output[str(item + '_vid')] = None
                output[str(item + '_id')] = case.contact_ids_dict[str(item)]
            output['clio_type'] = xxx['type'] 
            output['is_client'] = xxx['is_client']
            throughput.append(output)
          return throughput
        
def balien(xxx, case):
            output = {}
            output['id'] = xxx['id'] 
            output['name'] = {}
            name = output['name']
            if xxx['type'] == 'Company':
              name['text'] = xxx['name']
            else:
              name['first'] = xxx['first_name'] 
              name['middle'] = xxx['middle_name'] 
              name['last'] = xxx['last_name'] 
              output['firm'] = xxx['company']
              output['firm'] = {}
              company = xxx['company']
              firm = output['firm']
              firm['name'] = {}
              firmname = firm['name']
              if xxx['company'] is not None:
                firmname['text'] = company['name']
                output['phone'] = company['primary_phone_number']
                firm['id'] = company['id']
              if xxx['primary_address'] is not None:
                firm['address'] = {}
                yy = xxx['primary_address'] 
                zz = firm['address']
                zz['address'] = yy['street']
                zz['city'] = yy['city']
                zz['state'] = yy['province']
                zz['zip'] = yy['postal_code']
                zz['id'] = yy['id']
              else:
                output['address'] = None
            output['is_client'] = xxx['is_client'] 
            if xxx['email_addresses'] is not None:
              #email_list = []
              for mail in xxx['email_addresses']:
                if mail['primary'] == True:
                  #output['emails'] = {}
                  #emailz = output['emails'] 
                  output['email'] = mail['address']
                  #emailz['name'] = emails['name']
                  output['email_id'] = mail['id']
                  #email_list.append(emailz)
              if 'email' not in output:
                for mail in xxx['email_addresses']:
                  output['email_id'] = mail['id']
                  output['email'] = mail['address']
            output['phone'] = xxx['primary_phone_number'] 
            customs = xxx['custom_field_values']
            cust = []
            for q in customs:
              output[str(q['field_name'])] = q['value']
              output[str(q['field_name'] + '_vid')] = q['id']
              output[str(q['field_name'] + '_id')] = case.contact_ids_dict[str(q['field_name'])]
              cust.append(q['field_name'])
            #if output['is_lawyer'] is not None and output['is_lawyer'] == True:

            for item in case.clio_contact_customs:
              if item not in cust:
                output[str(item)] = None
                output[str(item + '_vid')] = None
                output[str(item + '_id')] = case.contact_ids_dict[str(item)]
            output['clio_type'] = xxx['type'] 
            output['is_client'] = xxx['is_client']
            
            return AliensInvade(output)
        
def prae_aliens(data, case):
          throughput = []
          throughput.clear()
          for xxx in data:
            output = {}
            output['id'] = xxx['id'] 
            output['name'] = {}
            name = output['name']
            if xxx['type'] == 'Company':
              name['text'] = xxx['name']
            else:
              name['first'] = xxx['first_name'] 
              name['middle'] = xxx['middle_name'] 
              name['last'] = xxx['last_name'] 
            if xxx['primary_address'] is not None:
              output['address'] = {}
              yy = xxx['primary_address'] 
              zz = output['address']
              zz['address'] = yy['street']
              zz['city'] = yy['city']
              zz['state'] = yy['province']
              zz['zip'] = yy['postal_code']
            else:
              output['address'] = None
            output['is_client'] = xxx['is_client'] 
            output['email'] = xxx['primary_email_address'] 
            output['phone'] = xxx['primary_phone_number'] 
            customs = xxx['custom_field_values']
            cust = []
            for q in customs:
              output[str(q['field_name'])] = q['value']
              output[str(q['field_name'] + '_vid')] = q['id']
              output[str(q['field_name'] + '_id')] = case.contact_ids_dict[str(q['field_name'])]
              cust.append(q['field_name'])
            if output['is_lawyer'] is not None and output['is_lawyer'] == True:
              if xxx['company'] is not None:
                output['firm'] = {}
                company = xxx['company']
                firm = output['firm']
                firm['name'] = {}
                firmname = firm['name']
                firmname['text'] = company['name']
                output['phone'] = company['primary_phone_number']
                firm['id'] = company['id']
              else: 
                output['firm'] = None
            for item in case.clio_contact_customs:
              if item not in cust:
                output[str(item)] = None
                output[str(item + '_vid')] = None
                output[str(item + '_id')] = case.contact_ids_dict[str(item)]
            output['clio_type'] = xxx['type'] 
            output['is_client'] = xxx['is_client']
            throughput.append(output)
          newlist = []
          for item in throughput:
            newlist.append(AliensInvade(item))
          return newlist
        
def parse_alien(matter_data, case):
          output = {}
          for xxx in matter_data:
            customs = xxx['custom_field_values']
            cust = []
            for q in customs:
              output[str(q['field_name'])] = q['value']
              output[str(q['field_name'] + '_vid')] = q['id']
              output[str(q['field_name'] + '_id')] = case.matter_ids_dict[str(q['field_name'])]
              cust.append(q['field_name'])
            #for item in case.clio_matter_customs:
              #if item not in cust:
                #output[str(item)] = None
                #output[str(item + '_vid')] = None
                #output[str(item + '_id')] = case.matter_ids_dict[str(item)]
            output['id'] = xxx['id']
            relationships = []
            for item in xxx['relationships']:
              relationships.append(item['id'])
            output['relationships'] = relationships
          return AliensInvade(output)

def facd_alien(xxx):
          output = {}
          custom = xxx['custom_field_values']
          #{‘id’: ‘checkbox-324694399’, ‘field_name’: ‘is_lawyer’, ‘custom_field’: {‘id’: 8235139, ‘etag’: ‘“7da88361381a6f6a68f6d0d2c3633492”’}}
          for q in custom:
            #field = q['custom_field']
            output[str(q['field_name'] + '_vid')] = q['id']
          output['id'] = xxx['id']
          output['clio_type'] = xxx['type']
          return AliensInvade(output)
        
def terrarize(contact, case):
          d = case.contact_ids_dict
          t = contact
          t.gender_id = d['gender']
          t.is_lawyer_id = d['is_lawyer']
          t.is_party_id = d['is_party']
          t.is_lawfirm_id = d['is_lawfirm'] 
          t.party_type_id = d['party_type']
          t.represents_id = d['represents'] 
          t.name.caption_type_id = d['caption_type'] 
          t.caption_text_id = d['caption_text']
          t.firms_id = d['firms']
          t.party_type_id = d['party_type']
          t.bar_number_id = case.contact_ids_dict['bar_number'] 
          t.state_bar_id = case.contact_ids_dict['state_bar']
          t.dba_id = case.contact_ids_dict['dba']
          t.trust_id = case.contact_ids_dict['trust']
          
def str_to_json(string):
  you = json.dumps(string)
  me = json.loads(string)
  return me

class AliensInvade(object):
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)
        self.from_dict(d)

    def from_dict(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = AliensInvade(value)
            self.__dict__[key] = value

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if type(value) is AliensInvade:
                value = value.to_dict()
            d[key] = value
        return d

    def __repr__(self):
        return str(self.to_dict())

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

def without_keys(d, keys):
  return {xxx: d[xxx] for xxx in d if xxx not in keys}

class ClioAuth(DAOAuth):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.appname = 'clio'
        self.token_uri = "https://app.clio.com/oauth/token"
        self.auth_uri = "https://app.clio.com/oauth/authorize"
        self.scope = "https://app.clio.com/api/v4/users/who_am_i"
    def authorize(self, web):
        headers = dict()
        self.get_credentials().apply(headers)
        if hasattr(web, 'headers'):
            web.headers.update(headers)
        else:
            web.headers = headers
            
class ClioZed(DAWeb):
  def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.base_url = 'https://app.clio.com/api/'

  def phone_home(self, case):
    try:
      payload = case.payload()
      home = self.patch('v4/matters/' + str(case.id) + '.json', data=payload)
    except DAWebError as e:
      log("Response from API: Failed to phone home because " + e.response_text)
      home = (False, False)
    return home
      
  def quaeroo(self, case, contact):
        try:  
          payload = {'fields':"custom_field_values{id, field_name, value}, id, name, first_name, middle_name, last_name, company{name, primary_phone_number, id}, primary_address{street, city, province, postal_code, name, id}, is_client, primary_email_address, primary_phone_number, type, email_addresses{id, name, address, primary}"}
          contactdata = self.get('v4/contacts/' + str(contact.id) + '.json', data=payload)
          dataa = contactdata['data']
          fields = balien(dataa, case)
        except DAWebError as e:
          log("Response from API: " + e.response_text)
          fields = (False, False)
        return fields
        
  def identify_custom_aliens(self):
        try:
          payload = {'fields':"name, id, parent_type, field_type"}
          data = self.get('v4/custom_fields.json', data=payload)
          log("Response from API: " + data)
          throughput = parse_alienids(data['data'])
        except DAWebError as e:
          log("Response from API: " + e.response_text)
          throughput = [False]
        return throughput

  def quaero_matter_contact_ids_w_type(self, case):
        try:  
          payload = {'fields':"id, name, first_name, middle_name, last_name, company{name, primary_phone_number, id}, primary_address{street, city, province, postal_code, name, id}, is_client, primary_email_address, primary_phone_number, type, custom_field_values{id, field_name, value}, email_addresses{id, address, name}, relationship{id}"}
          matter = self.get('v4/matters/' + str(case.id) + '/contacts.json', data=payload)['data']
          
          throughput = parse_aliens(matter, case)
        except DAWebError as e:
          log("Response from API: " + e.response_text)
          throughput = [False]
        return throughput
     
  def beam(self, contact, case):
      try:  
        payload = contact.payload(case)
        load = {'fields':"type, id, custom_field_values{id, field_name, value}"}
        getback = self.patch('v4/contacts/' + str(contact.id) + '.json', data=payload, params=load)['data']
        scotty = facd_alien(getback)
      except DAWebError as e:
        log("Response from API: failed to beam " + contact.name.full() + " up because " + e.response_text)
        scotty = False
      return scotty
    
  def praetento_contact1(self, quaero, case, cliotype):
        try:
          payload = {'fields':"id, name, first_name, middle_name, last_name, company{name, primary_phone_number, id}, primary_address{street, city, province, postal_code, name}, is_client, primary_email_address, primary_phone_number, type, custom_field_values{id, field_name, value}", 'query':str(quaero), 'type':str(cliotype)}
          contact = self.get('v4/contacts.json', data=payload)['data']
          #contact = self.get('v4/contacts.json', data=payload)
          #return contact
          if not contact:
            return False
          throughput = prae_aliens(contact, case)
        except DAWebError as e:
          log("Response from API to praetento_contact call for " + quaero + ":" + e.response_text)
          throughput = False
        return throughput
      
  def praetento_contact(self, quaero, case):
        try:
          payload = {'fields':"id, name, first_name, middle_name, last_name, company{name, primary_phone_number, id}, primary_address{street, city, province, postal_code, name}, is_client, primary_email_address, primary_phone_number, type, custom_field_values{id, field_name, value}", 'query':str(quaero)}
          contact = self.get('v4/contacts.json', data=payload)['data']
          #contact = self.get('v4/contacts.json', data=payload)
          #return contact
          if not contact:
            return False
          throughput = prae_aliens(contact, case)
        except DAWebError as e:
          log("Response from API to praetento_contact call for " + quaero + ":" + e.response_text)
          throughput = False
        return throughput
  
  def facio_contact(self, contact):
        try:
          payload = contact.facioload()
          motherload = {'fields':"id, name, first_name, middle_name, last_name, company{name, primary_phone_number, id}, primary_address{street, city, province, postal_code, name}, is_client, primary_email_address, primary_phone_number, type, custom_field_values{id, field_name, custom_field}"}
          data = self.post('v4/contacts.json', data=payload, params=motherload)['data']
          throughput = facd_alien(data)
          #{‘is_lawyer_vid’: 8235139, ‘is_party_vid’: 8235154, ‘is_lawfirm_vid’: 8278549, ‘caption_type_vid’: 8278564, ‘caption_text_vid’: 8278579, ‘firms_vid’: 8278594, ‘represents_vid’: 8278834, ‘division_vid’: 8305444, ‘district_vid’: 8305534, ‘county_vid’: 8305549, ‘state_vid’: 8305564, ‘gender_vid’: 8307904} 
        except DAWebError as e:
          log("Response from API to facio_contact call for " + contact.name.full() + ":" + e.response_text)
          throughput = [False]
        return throughput

      
  def post_custom_field(self, field_name, case):
        try:
          if field_name in case.clio_matter_customs:
            parent_type = "Matter"
          else:
            parent_type = "Contact"
          if field_name in ('is_party', 'is_lawyer', 'is_lawfirm'):
            field_type = "checkbox"
          elif field_name in ('doi', 'sol'):
            field_type = "date"
          else:
            field_type = "text_line"
          payload =  {'data': {"displayed": False, "field_type": str(field_type), "name": str(field_name), "parent_type": str(parent_type), "required": False}}
          pams = {'fields':"id, name"}
          material = self.post('v4/custom_fields.json', data=payload, params=pams)['data']
        except DAWebError as e:
          log("Response from API: post_custom_field failed to make " + field_name + ' because ' + e.response_text)
          material = False
        return material
  
  def quaero_material(self, quaero, case):
        try:
          matter = self.get('v4/matters.json', data={'query':str(quaero), 'fields':'description, id, etag, practice_area{id, name}, user{id, name}, relationships{id, description}, responsible_attorney{id, name}, custom_field_values{id, etag, field_name, field_type, value}'})['data']
          brains = parse_alien(matter, case)
        except DAWebError as e:
          log("Response from API: " + e.response_text)
          brains = False
        return brains
 
  def quaero_clio_customids(self, quaero, parent_type):
        try:
          material = self.get('v4/custom_fields.json', data={'query':str(quaero), 'parent_type': str(parent_type), 'fields':'id'})
          custom = material['data']
          if len(custom):
            output = custom[0]
          else:
            output = 'True'
        except DAWebError as e:
          log("Response from API: " + e.response_text)
          output = 'False'
        return output
    
  def single_matter(self, materialid, case):
        try:  
          matter = self.get('v4/matters/' + str(materialid) + '.json', data={'fields':'description, id, etag, practice_area{id, name}, user{id, name}, relationships{id, description}, responsible_attorney{id, name}, custom_field_values{id, etag, field_name, field_type, value}'})['data']
          brains = parse_alien(matter, case)
        except DAWebError as e:
          log("Response from API: " + e.response_text)
          brains = False
        return brains

  def quaero_rfp_id_from_clio(self, matterid):
        try:
          #Return the data for all DocumentCategories to get id for the user's folders/documents categorized as "Discovery "
          material = self.get('v4/document_categories.json', data={'fields':'id', 'query':'Discovery '})
          materialdata = material['data']
          materialid = materialdata
        except DAWebError as e:
          log("Response from API: " + e.response_text)
          materialid = False
        return materialid
  def something_deleted(self):
        try:
          #Return the data of the contents of a Folder to get all documents categorized as "RFP" or docs in a folder categorized as "Discovery " (at least I think it's both) for the particular matter.
          
          new_material = self.get('v4/documents.json', data={'fields':'filename, id, type', 'document_category_id':str(materialid['id']), 'matter_id':str(matterid)})
          new_data = new_material['data']
        except DAWebError as e:
          log("Response from API: " + e.response_text)
          new_data = False
        
        return new_data

class ClioLed(DAWeb):
  def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.base_url = 'https://app.clio.com/api/'

  def _call(self, url, method=None, data=None, params=None, headers=None, json_body=None, on_failure=None, on_success=None, auth=None, task=None, task_persistent=None, files=None, cookies=None, success_code=None):
        task = self._get_task(task)
        task_persistent = self._get_task_persistent(task_persistent)
        auth = self._get_auth(auth)
        json_body = self._get_json_body(json_body)
        on_failure = self._get_on_failure(on_failure)
        on_success = self._get_on_success(on_success)
        success_code = self._get_success_code(success_code)
        if isinstance(success_code, str):
            success_code = [int(success_code.strip())]
        elif isinstance(success_code, (abc.Iterable, DASet, DAList)):
            new_success_code = list()
            for code in success_code:
                if not isinstance(code, int):
                    raise Exception("DAWeb.call: success codes must be integers")
                new_success_code.append(code)
            success_code = new_success_code
        elif isinstance(success_code, int):
            success_code = [success_code]
        elif success_code is not None:
            raise Exception("DAWeb.call: success_code must be an integer or a list of integers")
        if method is None:
            method = 'GET'
        if not isinstance(method, str):
            raise Exception("DAWeb.call: the method must be a string")
        method = method.upper().strip()
        if method not in ('POST', 'GET', 'PATCH', 'PUT', 'HEAD', 'DELETE', 'OPTIONS'):
            raise Exception("DAWeb.call: invalid method")
        if not isinstance(url, str):
            raise Exception("DAWeb.call: the url must be a string")
        if not re.search(r'^https?://', url):
            url = self._get_base_url() + re.sub(r'^/*', '', url)
        if data is None:
            data = dict()
        if isinstance(data, DADict):
            data = data.elements
        if json_body is False and not isinstance(data, dict):
            raise Exception("DAWeb.call: data must be a dictionary")
        if params is None:
            params = dict()
        if isinstance(params, DADict):
            params = params.elements
        if not isinstance(params, dict):
            raise Exception("DAWeb.call: params must be a dictionary")
        if headers is None:
            headers = dict()
        if isinstance(headers, DADict):
            headers = headers.elements
        if not isinstance(headers, dict):
            raise Exception("DAWeb.call: the headers must be a dictionary")
        headers = self._get_headers(headers)
        if len(headers) == 0:
            headers = None
        if cookies is None:
            cookies = dict()
        if isinstance(cookies, DADict):
            cookies = cookies.elements
        if not isinstance(cookies, dict):
            raise Exception("DAWeb.call: the cookies must be a dictionary")
        cookies = self._get_cookies(cookies)
        if len(cookies) == 0:
            cookies = None
        if isinstance(data, dict) and len(data) == 0:
            data = None
        if files is not None:
            if not isinstance(files, dict):
                raise Exception("DAWeb.call: files must be a dictionary")
            new_files = dict()
            for key, val in files.items():
                if not isinstance(key, str):
                    raise Exception("DAWeb.call: files must be a dictionary of string keys")
                try:
                    path = server.path_from_reference(val)
                    logmessage("path is " + str(path))
                    assert path is not None
                except:
                    raise Exception("DAWeb.call: could not load the file")
                new_files[key] = open(path, 'rb')
            files = new_files
            if len(files):
                json_body = False
        try:
            if method == 'POST':
                if json_body:
                    r = requests.post(url, json=data, params=params, headers=headers, auth=auth, cookies=cookies, files=files)
                else:
                    r = requests.post(url, data=data, params=params, headers=headers, auth=auth, cookies=cookies, files=files)
            elif method == 'PUT':
                if json_body:
                    r = requests.put(url, json=data, params=params, headers=headers, auth=auth, cookies=cookies, files=files)
                else:
                    r = requests.put(url, data=data, params=params, headers=headers, auth=auth, cookies=cookies, files=files)
            elif method == 'PATCH':
                if json_body:
                    r = requests.patch(url, json=data, params=params, headers=headers, auth=auth, cookies=cookies, files=files)
                else:
                    r = requests.patch(url, data=data, params=params, headers=headers, auth=auth, cookies=cookies, files=files)
            elif method == 'GET':
                if len(params) == 0:
                    params = data
                    data = None
                r = requests.get(url, params=params, headers=headers, auth=auth, cookies=cookies)
            elif method == 'DELETE':
                if len(params) == 0:
                    params = data
                    data = None
                r = requests.delete(url, params=params, headers=headers, auth=auth, cookies=cookies)
            elif method == 'OPTIONS':
                if len(params) == 0:
                    params = data
                    data = None
                r = requests.options(url, params=params, headers=headers, auth=auth, cookies=cookies)
            elif method == 'HEAD':
                if len(params) == 0:
                    params = data
                    data = None
                r = requests.head(url, params=params, headers=headers, auth=auth, cookies=cookies)
        except RequestException as err:
            if on_failure == 'raise':
                raise DAWebError(url=url, method=method, params=params, headers=headers, data=data, task=task, task_persistent=task_persistent, status_code=-1, response_text='', response_json=None, response_headers=dict(), exception_type=err.__class__.__name__, exception_text=str(err), cookies_before=cookies, cookies_after=None)
            else:
                return on_failure
        if success_code is None:
            if r.status_code >= 200 and r.status_code < 300:
                success = True
            else:
                success = False
        else:
            if r.status_code in success_code:
                success = True
            else:
                success = False
        if hasattr(self, 'cookies'):
            self.cookies = dict(r.cookies)
        try:
            json_response = r.json()
        except:
            json_response = None
        if success and task is not None:
            mark_task_as_performed(task, persistent=task_persistent)
        if not success:
            if on_failure == 'raise':
                raise DAWebError(url=url, method=method, params=params, headers=headers, data=data, task=task, task_persistent=task_persistent, status_code=r.status_code, response_text=r.text, response_json=json_response, response_headers=r.headers, exception_type=None, exception_text=None, cookies_before=cookies, cookies_after=dict(r.cookies), success=success)
            else:
                return on_failure
        if success and on_success is not None:
            if on_success == 'raise':
                raise DAWebError(url=url, method=method, params=params, headers=headers, data=data, task=task, task_persistent=task_persistent, status_code=r.status_code, response_text=r.text, response_json=json_response, response_headers=r.headers, exception_type=None, exception_text=None, cookies_before=cookies, cookies_after=dict(r.cookies), success=success)
            else:
                return on_success
        return(json_response if json_response is not None else r.content)
  

  def quaero_rfp_from_clio(self, rfp_id):
      try:
            r2 = self.get('v4/documents/' + str(rfp_id) + '/download.json')
            r1 = DAFile('r1')
            r1.initialize(filename='r1.pdf')
            #r2 = DAFile('r2')
            #r2.initialize(filename='r2.pdf')
            r1.set_attributes(private=False)
          
            r1.write(r2, binary=True)
            r1.commit()
            r1.retrieve()
            r3 = ocr_file_in_background(r1)
            #r1.save(r1.path())
            #r1.commit()
            #r1.retrieve()
      except DAWebError as e:
            log("Response from API: " + e.response_text)
            r3 = False
      return (r3)
# Trial Legend ©2021 Scott Cumming - ALL RIGHTS RESEVERED.
    def impetra_rfas(self, client):
        output = SCList('impetra_rfas', there_are_any=True, auto_gather=False)
        output.clear()
        output.append(str("Admit that "  + self.recipients().pnameu_possessive() + " " self.fault + " caused the " + self.incident() + " in one or more of the ways alleged in the " + client.pleading() + "."))

        output.append(str("Admit that " +self.recipients().pnameu() + " " + self.recipients().did_verb('were') + " " + self.at_fault + " in one or more of the ways alleged in the " + client.pleading() + "."))

        for exhibit in self.rfas.exhibits(client, self.exhibits_list):
          if exhibit.is_business_record:
            output.append(str("Admit that Exhibit " + str(self.rfas.exhibits(client, self.exhibits_list).index(exhibit)+1) + " is a copy of business records of " + exhibit.author +"."))
          if exhibit.is_true_and_accurate:
            output.append(str("Admit that Exhibit " + str(self.rfas.exhibits(client, self.exhibits_list).index(exhibit)+1) + " is an authentic duplicate, reproduction, or original copy of " + exhibit.author+"."))
          if exhibit.is_public_record:
            output.append(str("Admit that Exhibit " + str(self.rfas.exhibits(client, self.exhibits_list).index(exhibit)+1) + " is a public record of " + exhibit.author + "."))
          if exhibit.is_medical_bills:
            output.append(str("Admit that the " + self.incident+ " caused " + client.pnameu() + " to sustain at least " + currency(self.damages.ecomonomics.past_meds.total()) + " in economic damages for medical and other health care expenses, as evidenced in Exhibit " + str(self.rfas.exhibits(client, self.exhibits_list).index(exhibit)+1) + "."))
            output.append(str("Admit that the medical and other health care expenses listed in Exhibit " + str(self.rfas.exhibits(client, self.exhibits_list).index(exhibit)+1)  + " were reasonable in charge for " + client.address.city + ", " + state_name(client.address.state)+ " and similar communities for the services provided.")
            output.append(str("Admit that the treatment for which the medical and other health care expenses listed in Exhibit " +  str(self.rfas.exhibits(client, self.exhibits_list).index(exhibit)+1) + " relate was necessitated by " + client.pnameu_possessive() + " injuries and symptoms that were caused by the " + self.incident+ "."))
          if exhibit.is_medical_records:
            output.append(str("Admit that all treatment for which the medical and other health care expenses listed in Exhibit " + str(self.rfas.exhibits(client, self.exhibits_list).index(exhibit)+1)  + " relate was reasonable for symptoms " + client.pnameu() + " was " + " experiencing at the applicable times.")
        if client.was_injured():
          for injury in client.injuries():
            output.append(str("Admit that the " + self.incident + " caused " + client.asnoun() + " " + possessify(client.name.full(), "") + injury[0].lower() + injury[1:] + "."))
            if not injury.was_preexisting:
              output.append(str("Admit that " + client.asnoun() + " " + client.name.full() + " did not have " + injury[0].lower() + injury[1:] + " immediately preceding the " + self.incident +"."))
            for provider in providers(client)
              output.append(str("Admit that the treatment " + client.asnoun() + " " + client.name.full().upper() + " received at " + provider.name.full() + " from " + provider.dos[0] + " until " + provider.dos[-1] + " was reasonable and necessitated by the injuries " + client.asnoun() + " " + client.name.full().upper() + " sustained from the " + self.incident + "."))
        if client.has_noneconomics():
            output.append(str("Admit the " + self.incident+ " caused " + self.user_clientlist().pnameu() + " to incur **some** noneconomic damages.")
        if client.has_economics():
          if self.property_was_damaged():
            for property_damage in self.damages.economics.property:
              output.append(str("Admit that the " + self.incident + " caused approximately " + self.currency(property_damage.estimated_damage)+ " in property damage to " + property_damage.name.text +"."))
              

        if client.has_reduced_earning_capacity:
          output.append(str("Admit that " + client.pnameu_possessive() + " symptoms after the " + self.incident + " caused " + client.pronoun_objective() + " to sustain some impairment of " + client.pronoun_possessive("earning capacity")+"."))

        if client.has_lost_wages():
          output.append(str("Admit that " + client.pnameu_possessive() + " symptoms after the " + self.incident+ " caused " + client.pronoun_objective()+ " to sustain some lost wages.")

        if self.is_premises_liability():
          output.append(str("Admit that, at the time of the " + self.incident + ", " + self.the_hazard.lower() + " at issue constituted an unreasonably dangerous condition.")

          output.append(str("Admit that, at the time of the " + self.incident + ", it was reasonably foreseeable that other people attempting to walk on the subject area where " + client.pnameu() + " fell would not discover or realize the extent of the danger that " + self.the_hazard.lower() + " comprised.")
                      
        output.there_is_another = False
        output.gathered = True
        return output
                          
    def rfa_outro(self):
      output = str("If " + self.recipients().asnoun() + " " + self.recipients().does_verb('fail') + " to admit the truth of the above, " + self.user_clientlist().asnoun() + " will apply to the Court for an Order requiring " + self.recipients().asnoun() + " to pay the reasonable expenses of making such proof at trial, including expert witness fees and attorney’s fees, pursuant to " + self.rfa_sanction_rule + ".")
      return output
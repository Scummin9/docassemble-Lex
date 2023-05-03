  @property
  def mva_specs(self):
    if 'rear end' in self.crash_type:
      output.append("In following " + self.the_ps().nameu_possessive() + ",  vehicle closer than reasonable and prudent under the circumstances then and there existing " + str("(negligence *per se*, ORS 811.485)" if self.juris.state.name.text =="Oregon" else ""))
    output.append("In driving at a speed greater than reasonable under the circumstances then and there existing " + str("(negligence per se, ORS 811.100)" if self.juris.state.name.text =="Oregon" else ""))
    output.append("In failing to keep a proper lookout")
    output.append("In failing to keep proper control of his vehicle")
    output.append("In failing to sound " + self.the_bullets().pronoun_possessive("") + " horn or otherwise warn " + self.the_ps().nameu_possessive() + " of the impending collision")
    output.append("In failing to drive at a speed that is reasonable and prudent under the circumstances")
    output.append("In failing to stop short of, or otherwise take evasive maneuvers to avoid colliding into, " + self.the_ps().nameu_possessive() + "vehicle")
    if self.dui:
      output.append("In driving while under the influence of intoxicants " + str("(negligence *per se*, ORS 813.010)" if self.juris.state.name.text =="Oregon" else ""))
      output.append("In recklessly causing serious physical injury to " + self.the_ps().nameu + " " + str("(negligence *per se*, ORS 163.165(2))" if self.juris.state.name.text =="Oregon" else ""))
      output.append("In drinking alcohol to the point of intoxication when " + self.the_bullets().pronoun_subjective() + " knew, or should have known, that " + self.the_bullets().pronoun_subjective() + " was likely to drive on a public roadway shortly thereafter")
    if self.was_speeding:
      output.append("In driving " + self.the_bullets().pronoun_possessive("") + " in excess of the posted speed limit " + str("(negligence *per se*, ORS 811.100–111)" if self.juris.state.name.text =="Oregon" else ""))
    if self.rear_ended:
      output.append("In following " + self.the_ps().nameu_possessive() + " vehicle closer than reasonable and prudent under the circumstances then and there existing " + str("(negligence *per se*, ORS 811.485)" if self.juris.state.name.text =="Oregon" else ""))
    if self.tried_to_turn:
      output.append("In impeding the normal and reasonable movement of traffic " + str("(negligence *per se*, ORS 811.130)" if self.juris.state.name.text =="Oregon" else ""))
      if self.turned_right:
        output.append("In attempting to turn to the right when said movement could not be made with reasonable safety " + str("(negligence *per se*, 811.335)" if self.juris.state.name.text =="Oregon" else ""))
      if self.turned_left:
        output.append("In making a left turn when the movement could not be made with reasonable safety " + str("(negligence *per se*, ORS 811.335(1)(a))" if self.juris.state.name.text =="Oregon" else ""))
        output.append("In making a left turn without giving an appropriate signal continuously for not less than the last 100 feet travelled by " + self.the_bullets().pronoun_possessive("") + "vehicle before turning " + str("(negligence per se, ORS 811.335(1)(b))" if self.juris.state.name.text =="Oregon" else ""))
        output.append("In failing to approach the point of " + self.the_bullets().pronoun_possessive("") + "left turn in the extreme left-hand lane lawfully available to traffic moving in the direction of travel of " + self.the_bullets().pronoun_possessive("") + "vehicle " + str("(negligence *per se*, ORS 811.340)" if self.juris.state.name.text =="Oregon" else ""))
        output.append("In failing to use the special left turn lane when initiating " + self.the_bullets().pronoun_possessive("") + "turn " + str("(negligence *per se*, ORS 811.345)" if self.juris.state.name.text =="Oregon" else ""))
        output.append("In misusing the special left turn lane in using said lane of a purpose other than to make a left turn either into or from " + str("(negligence *per se*, ORS 811.346)" if self.juris.state.name.text =="Oregon" else ""))
    if self.illegal_uturn:
      output.append("In attempting a U-turn between intersections " + str("(negligence *per se*, ORS 811.365)" if self.juris.state.name.text =="Oregon" else ""))
    if self.tried_to_merge:
      output.append("In failing to operate " + self.the_bullets().pronoun_possessive("") + "vehicle within a single lane of travel and refrain from leaving that lane until  " + self.the_bullets().pronoun_subjective() + " had first made certain that the movement could be made with safety " + str("(negligence *per se*, ORS 811.370)" if self.juris.state.name.text =="Oregon" else ""))
      output.append("In changing lanes when the movement could not be made with reasonable safety " + str("(negligence *per se*, ORS 811.375(1)(a))" if self.juris.state.name.text =="Oregon" else ""))
      output.append("In changing lanes without giving an appropriate signal continuously for not less than the last 100 feet travelled by " + self.the_bullets().pronoun_possessive("") + "vehicle before doing so " + str("(negligence *per se*, ORS 811.375(1)(b))" if self.juris.state.name.text =="Oregon" else ""))
    if self.failed_to_yield_right_of_way:
      output.append("In impeding traffic that was proceeding on " + self.mva.address.address + " " + str("(negligence *per se*, ORS 811.130)" if self.juris.state.name.text =="Oregon" else ""))
      output.append("In failing to yield the right of way to " + self.the_ps().nameu_possessive() + " vehicle when it was so close as to constitute an immediate hazard " + str("(negligence *per se*, ORS 811.280)" if self.juris.state.name.text =="Oregon" else ""))
    if 'speeding' in self.driver_factors:
      output.append("In exceeding the speed limit " + str("in a school zone" if 'school' in self.special_zone else "") + " (negligence *per se*, ORS 811.111" + str("; ORS 811.235)" if 'school' in self.special_zone else ")"))

    if 'wrong way' in self.driver_factors:
      output.append("In failing to drive on the right half of the roadway (negligence *per se*, ORS 811.295)")


    for party in self.parties:
      if party.is_complainant and party.has_thin_skull:
        output.append(str("At all times material, " + party.name.full().upper() + " had " + party.thin_skull_parts.as_noun('bodily condition', article=True) + " of " + party.pronoun_possessive("") + comma_and_list(party.thin_skull_parts) + " that made " + party.pronoun_objective() + " more susceptible to injury than a person in normal health, and " + party.pronoun_subjective() + " was injured as a result of " + party.thin_skull_parts.as_noun('condition', this=True)  + "."))


As a result of Defendant{% if defendant|length >=2 %}s’{% else %}’s{% endif %} " + type_of_fault + ", " + party.name.full().upper() + " sustained the following injuries and damages, all of which were reasonably foreseeable, and some of which may be permanent:
(a)	Damage to the muscles, ligaments, tendons, nerves, and other soft tissue of the " + comma_and_list(damage_parts) + ";
(b)	{%p for diagnosis in diagnosis|add_separators(last_separator=‘;’, end_mark=‘;’) %}
(c)	diagnosis[0].upper() + "" + diagnosis[1:] + "
(d)	{%p endfor %} 
(e)	Pain, discomfort, and suffering; and
(f)	Inconvenience and interference with usual and everyday activities, apart from gainful employment.
All to " + party.name.full()[0].possessive(‘’).upper() + " noneconomic damage in an amount determined by the jury to be fair and reasonable, but not to exceed the sum of " + currency(damages['noneconomic']) + ".
{%p if ‘Wrongful Death’ in claims %}
28.
" + party.name.full()[0].sub.upper() + " is survived by {% for survivors in survivors|add_separators %}" + party.name.full().pronoun_possessive(survivors.rel) + " " + survivors + "{% endfor %}. As a result of " + party.name.full()[0].possessive(‘’) + "death, " + party.name.full().pronoun_possessive(‘family’) + " has and will suffer noneconomic damages for loss of society and companionship in an amount to be determined by the jury to be fair and reasonable, but not to exceed the sum of " + currency(damages[‘wrongful death’]) + ", all of which was reasonably foreseeable.
{%p endif %} 
29.
As a result of the fault of Defendant{% if defendant|length >=2 %}s’{% else %}’s{% endif %} " + type_of_fault + ", " + party.name.full().upper() + " has sustained the following economic damages, all of which were reasonably foreseeable:
(a)	{%p if damages['economic'][‘Past Meds’]|int >0 %}
(b)	Reasonable and necessary medical expenses to date in the approximate sum of " + currency(damages['economic'][‘Past Meds’]) + "; 
(c)	{%p endif %} 
(d)	{%p if damages['economic']['Future Meds']|int >0 %}
(e)	Future reasonable and necessary medical expenses in an amount to be determined at the time of trial, but for the purposes of ORCP 18, estimated to be " + currency
(damages['economic']['Future Meds']) + "; 
(f)	{%p endif %} 
(g)	{%p if damages['economic']['Lost Wages']|int >0 %}
(h)	Lost income to date in the approximate sum of " + currency
(damages['economic']['Lost Wages']) + ";
(i)	{%p endif %} 
(j)	{%p if damages['economic']['Earning Capacity']|int >0 %}
(k)	Future impairment of earning capacity in an amount to be determined at the time of trial, but for the purposes of ORCP 18, estimated to be " + currency
(damages['economic']['Earning Capacity']) + ".
(l)	{%p endif %} 
(m)	{%p if ‘Wrongful Death’ in claims %}
(n)	Pecuniary loss in the approximate sum of " + currency(damages['pecuniary losses']) + ";
(o)	Mortuary, funeral and burial expenses in the approximate sum of " + currency(damages['mortuary']) + ";
(p)	{%p endif %}
All to " + party.name.full()[0].possessive(‘’) + " economic damages in an amount determined by the jury to be fair and reasonable, but not to exceed the sum of " + currency
(economic_total) + ".
{%p if party.name.full().is_medically_stationary == ‘False’ %}
30.
" + party.name.full().upper() + " hereby gives notice that " + party.name.full().pronoun_subjective() + " is not medically stationary and is still receiving treatment for " + party.name.full(). pronoun_possessive(‘injuries’) + ".  Therefore, the amounts alleged above are subject to change, pending " + party.name.full().pronoun_possessive(‘continued’) + " symptoms, treatment and ultimate prognosis.
{%p endif %} 

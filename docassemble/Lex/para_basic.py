
    if party.name.caption_type == 'business entity':
    if party.name.caption_type ==
{%p for index in range(defendant|length) %} 
{%p if defendant[index].type == ‘Governmental Entity’ %}
6.

{%p elif defendant[index].type == ‘Business Entity’ %}
{%p if defendant[index].businessentity == ‘Assumed Business Name’ %}
9.
	output.append(str("At all times material, Defendant " + defendant[index].individualdba|upper + " was {% if  defendant[index].business_status == “Active” %}and is {% endif %}an individual doing business as “" + defendant[index]|upper + ".”"))
10.
	output.append(str("At all times material, Defendant " + defendant[index].individualdba|upper + " had employed owners, officers, directors, members, managers, employees, agents, or others within its control, or right of control, and all of whom were acting within the course and scope of said positions. All acts or omissions attributed to Defendant " + defendant[index].individualdba|upper + " were either performed by " + defendant[index].individualdba|upper + ", or were otherwise performed by said persons in said capacities."))
{%p else %}
11.
	output.append(str("At all times material, Defendant " + defendant[index]|upper + " was {% if  defendant[index].business_status == “Active” %}and is {% endif %}{% if defendant[index].businessentity == ‘Foreign Nonprofit Corporation’ or defendant[index].businessentity == ‘Foreign Business Corporation’ or defendant[index].businessentity == ‘Foreign Professional Corporation’ %}" + indefinite_article(state_name(defendant[index].stofinc)) + " " + defendant[index].businessentity.lower() + " {% else %}" + indefinite_article(defendant[index].businessentity.lower()) + "{% endif %}{% if  defendant[index].orauthorized %}, authorized to transact business in the state of Oregon as " + indefinite_article(defendant[index].orauthorized) + "{% else %}, authorized to transact business for profit in the state of Oregon{% endif %}."))
		{%p if defendant[index].address.state == ‘OR’ %}
{%p if defendant[index].ppb_diff %} 
12.
	output.append(str("At all times material, Defendant " + defendant[index]|upper + " conducted{% if  defendant[index].business_status == “Active” %} and continues to conduct{% endif %} said business from its principal place of business/principal office located at " +  defendant[index]. ppb_address|title + ", {% if defendant[index]. ppb_unit %}" + defendant[index].ppb_unit + ", {% endif %}" + defendant[index].ppb_city|title + ", " + state_name(defendant[index].ppb_state) + " " + defendant[index]. ppb_zip + "."))
{%p else %}
13.
	output.append(str("At all times material, Defendant " + defendant[index]|upper + " conducted{% if  defendant[index].business_status == “Active” %} and continues to conduct{% endif %} said business from its principal place of business/principal office located at " +  defendant[index].address.address|title + ", {% if defendant[index].address.unit %}" + defendant[index].address.unit + ", {% endif %}" + defendant[index].address.city|title + ", " + state_name(defendant[index].address.state) + " " + defendant[index].address.zip + "."))
{%p endif %} 
		{%p endif %}
14.
	output.append(str("At all times material, Defendant " + defendant[index]|upper + " had working for it owners, officers, directors, members, managers, employees, agents, or others within its control, or right of control, and all of whom were acting within the course and scope of said positions.  All acts or omissions attributed to Defendant " + defendant[index]|upper + "  were performed by said persons in said capacities."))
{%p endif %}
{%p endif %} 

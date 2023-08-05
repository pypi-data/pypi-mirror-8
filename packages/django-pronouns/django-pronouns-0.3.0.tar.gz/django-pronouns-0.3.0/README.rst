==============================================
django-pronouns - Correctly address your users
==============================================

Pronouns are tricky. Writing correspondence or copy with your users preferred pronoun in mind is even harder.
Wanting to break out of the gender binary damn near impossible - until now. ``django-pronouns`` is here to help!

When a user is signing up, they can select their preferred pronouns (usually disguised as a gender option).
The usual suspects (s/he) are there, as well as more neutral ones (they, it, xir, etc). Using them in your
copy is as simple as working out which form you need, and ``django-pronouns`` will do the rest. Observe:

.. code:: python

	>>> "{{ user.pronoun.subject|title }} is awesome."
	"She is awesome."

	>>> "It is {{ user.name|pluralize }} birthday today. Go wish {{ user.pronoun.object }} a happy birthday!"
	"It is Tims birthday today. Go wish him happy birthday!"

	>>> "{{ user.name }} looked at {{ user.pronoun.reflexive }} in the mirror."
	"Alex looked at himself in the mirror."

	>>> "{{ user.pronoun.possessive_determiner|title }} stuff is on the table."
	"Her stuff is on the table."

	>>> "This guitar is {{ user.pronoun.possessive_pronoun }}."
	"This guitar is hers."

If working out which form is too annoying, we can help there as well. Each of the five forms has a number of
aliases, consisting of the feminine and masculine forms joined with an underscore, as well as the (new) Spivak
forms:

* **Subject**: ``he_she``, ``shen_he``, ``ey``
* **Object**: ``him_her``, ``her_him``, ``em``
* **Reflexive**: ``himself_herself``, ``herself_himself``, ``emself``
* **Possessive determiner**: ``his_her``, ``her_his``, ``eir``
* **Possessive pronoun**: ``his_hers``, ``hers_his``, ``eirs``

The female and male pronouns are combined, as by themselves they are ambiguous. ``his`` may refer to either the
possessive determiner, or the possessive pronoun, while ``her`` may refer to a possessive determiner or an
objective form. Spivak was chosen as it is one of the only forms that is unambiguous across all five forms.

Installing
==========

Install via pip:

.. code:: sh

	$ pip install django-pronouns

Add it to your ``INSTALLED_APPS`` in Django:

.. code:: python

	INSTALLED_APPS = (
		# ...
		"django_pronouns",
		# ...
	)

And finally, add the default pronoun set, if you want:

.. code:: sh

	$ python manage.py loaddata pronouns

You can edit these pronouns, add more, or remove some later, via the administration area.

Using
=====

Simply add a ``ForeignKey`` link to the Pronoun model to add pronouns to any model. Pronouns work very well when coupled with a UserProfile:

.. code:: python

	from django.db import models
	from django.contrib.auth.models import User

	from django_pronouns.models import Pronoun

	class UserProfile(models.Model):
		user = models.OneToOneField(User)

		name = models.CharField(max_length=255)
		dob = models.DateField()
		pronoun = models.ForeignKey(Pronoun)

Use them like you would any other ForeignKey in forms.

In your templates, you can request any of the pronoun forms:

.. code:: html+django

	{{ user.pronoun.subject|title }} is awesome.

	It is {{ user.name|pluralize }} birthday today. Go wish {{ user.pronoun.object }} happy birthday!

	{{ user.name }} looked at {{ user.pronoun.reflexive }} in the mirror.

	{{ user.pronoun.possessive_determiner|title }} stuff is on the table.

	This guitar is {{ user.pronoun.possessive_pronoun }}.

A bunch of shortcut have also been provided, as working out which form to use is annoying. Each of the five forms has a
number of aliases, consisting of the feminine and masculine forms joined with an underscore, as well as the Spivak
forms:

* **Subject**: ``he_she``, ``she_he``, ``ey``
* **Object**: ``him_her``, ``her_him``, ``em``
* **Reflexive**: ``himself_herself``, ``herself_himself``, ``emself``
* **Possessive determiner**: ``his_her``, ``her_his``, ``eir``
* **Possessive pronoun**: ``his_hers``, ``hers_his``, ``eirs``

Using them is the same as using the names forms:

.. code:: html+django

	{{ user.pronoun.she_he|title }} is awesome.

	It is {{ user.name|pluralize }} birthday today. Go wish {{ user.pronoun.him_her }} a happy birthday!

	{{ user.name }} looked at {{ user.pronoun.emself }} in the mirror.

	{{ user.pronoun.his_her|title }} stuff is on the table.

	This guitar is {{ user.pronoun.hers_his }}.

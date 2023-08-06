ChangeLog
=========

0.9.4 (2014-11-24)
------------------

*Bugfix:*

    * Add support for ``django.db.migrations`` (Django >= 1.7)

0.9.3 (2014-06-04)
------------------

*Packaging:*

    * #12: Prevent 'egg' packaging


0.9.2 (2013-09-25)
------------------

*Bugfix:*

    * Fix migrations to take into account Django's ``AUTH_USER_MODEL`` setting.

0.9.1 (2013-08-14)
------------------

*Bugfix:*

    * Fix packaging

0.9.0 (2013-05-16)
------------------

*New:*

    * #10: Ask Django' templates to not call transitions, and give access to sub-methods
      (e.g :meth:`~xworkflows.base.ImplementationWrapper.is_available`).
      Contributed by `kanu <https://github.com/kanu>`_.

0.8.1 (2012-11-30)
------------------

*Bugfix:*

    * #7: allow more than one :class:`~django_xworkflows.models.GenericTransitionLog` in the same project.


0.8.0 (2012-10-12)
------------------

*New:*

    * Provide a base :class:`~django_xworkflows.models.BaseLastTransitionLog` and a :class:`~django_xworkflows.models.GenericLastTransitionLog`,
      useful for storing only the *last* transition log for a given model.

0.7.1 (2012-09-10)
------------------

*Bugfix:*

    * Use :meth:`django.utils.timezone.now` instead of :meth:`datetime.datetime.now` with Django >= 1.4

0.7.0 (2012-08-17)
------------------

*New:*

    * Provide a base :class:`~django_xworkflows.models.BaseTransitionLog` without :class:`~django.contrib.contenttypes.generic.GenericForeignKey`.
    * Ease specification of transition kwargs to store in custom :class:`TransitionLog <django_xworkflows.models.BaseTransitionLog>` classes
    * Allow settings :attr:`~django_xworkflows.models.Workflow.log_model_class` explicitly (thus bypassing the lookup performed by
      :attr:`~django_xworkflows.models.Workflow.log_model`).

0.6.0 (2012-08-02)
------------------

*New:*

    * Enable support for `XWorkflows 0.4.0 <http://pypi.python.org/pypi/xworkflows/0.4.0/>`_

0.5.0 (2012-07-14)
------------------

*New:*

    * Add rebuild_transitionlog_states management command to refill :attr:`~django_xworkflows.models.BaseTransitionLog.from_state`
      and :attr:`~django_xworkflows.models.BaseTransitionLog.to_state`.
    * Add indexes on various :class:`django_xworkflows.models.BaseTransitionLog` fields

*Bugfix:*

    * Fix :class:`django_xworkflows.models.WorkflowEnabled` inheritance

0.4.5 (2012-06-12)
------------------

*Bugfix:*

    * Don't default to :class:`~django_xworkflows.models.TransactionalImplementationWrapper` when using
      a :class:`django_xworkflows.models.Workflow`.

0.4.4 (2012-05-29)
------------------

*Bugfix:*

    * Serialize unicode of :attr:`xworkflows.base.State.title` in south ORM freezing.

0.4.3 (2012-05-29)
------------------

*Bugfix:*

    * Include migrations in package

0.4.2 (2012-05-29)
------------------

*Bugfix:*

    * Fix log=False/save=False when calling transitions

0.4.1 (2012-05-29)
------------------

*Bugfix:*

    * Avoid circular import issues when resolving :attr:`~django_xworkflows.models.Workflow.log_model`
      to a :class:`~django.db.models.Model`
    * Log source and target state names in :class:`~django_xworkflows.models.BaseTransitionLog`

0.4.0 (2012-04-29)
------------------

*New:*

    * Improve south support
    * Run transition implementations in a database transaction

0.3.1 (2012-04-15)
------------------

*New:*

    * Introduce :class:`~django_xworkflows.models.StateField` for adding a :class:`~django_xworkflows.models.Workflow`
      to a model
    * Adapt to xworkflows-0.3.0

.. vim:et:ts=4:sw=4:tw=79:ft=rst:

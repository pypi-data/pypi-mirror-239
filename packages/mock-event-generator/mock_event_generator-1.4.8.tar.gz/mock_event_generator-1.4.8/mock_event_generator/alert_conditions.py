"""Utility and setting of the alert conditions.

To be used (in future in gwcelery)
Implement:
- is_significant(event: dict[str, Any]) -> bool
- should_publish(event: dict[str, Any]) -> bool
"""

from typing import Any


class AlertConditions:
    """Class that define the threshould for alerts.

    The value are determined by the ``thresholds`` static dictionary.
    """

    one_day = 1 / 3600 / 24
    one_month = 1 / 3600 / 24 / 30
    one_year = 1 / 3600 / 24 / 365
    thresholds_cbc = 2 * one_day
    thresholds_burst = 2 * one_day
    thresholds: dict[tuple[str, str, str], tuple[float, float]] = {
        # CBC AllSKy searches
        ('cbc', 'mbta', 'allsky'): (2 * one_day, one_month / 6),
        ('cbc', 'gstlal', 'allsky'): (2 * one_day, one_month / 6),
        ('cbc', 'pycbc', 'allsky'): (2 * one_day, one_month / 6),
        ('cbc', 'spiir', 'allsky'): (2 * one_day, one_month / 6),
        # CBC EarlyWarning searches
        ('cbc', 'mbta', 'earlywarning'): (one_month, one_month / 6),
        ('cbc', 'gstlal', 'earlywarning'): (one_month, one_month / 6),
        ('cbc', 'pycbc', 'earlywarning'): (one_month, one_month / 6),
        ('cbc', 'spiir', 'earlywarning'): (one_month, one_month / 6),
        # CBC SSM searches
        ('cbc', 'mbta', 'ssm'): (one_month / 6, one_year / 4),
        ('cbc', 'gstlal', 'ssm'): (one_month / 6, one_year / 4),
        # BURST BBH searches
        ('burst', 'cwb', 'bbh'): (2 * one_day, one_month / 6),
        # BURST AllSky searches
        ('burst', 'cwb', 'allsky'): (2 * one_day, one_year / 4),
        ('burst', 'olib', 'allsky'): (2 * one_day / 6, one_year / 4),
        # CBC MDC gstlal
        ('cbc', 'gstlal', 'mdc'): (2 * one_day, one_month / 6),
    }

    def get_far(self, group: str, pipeline: str, search: str) -> float:
        """Method that return the far threshould for generating alerts.

        Parameters
        ----------
        group : str
        pipeline : str
        search : str

        Returns
        -------
        far : float
        """
        return self.thresholds.get((group, pipeline, search), (0.0, 0.0))[0]

    def get_significant_far(self, group: str, pipeline: str, search: str) -> float:
        """Method that return the far threshould for significant alerts.

        Parameters
        ----------
        group : str
        pipeline : str
        search : str

        Returns
        -------
        far : float
        """
        return self.thresholds.get((group, pipeline, search), (0.0, 0.0))[1]


alert_conditions = AlertConditions()


def is_significant(event: dict[str, Any]) -> bool:
    """Determine whether an event should be considered a significant event.

    All of the following conditions must be true for a public alert:

    *   The event's ``offline`` flag is not set.
    *   The event's is not an injection.
    *   The event's false alarm rate is less than or equal to
        :obj:`~gwcelery.conf.alert_far_thresholds`

    or the event has been marked to generate a RAVEN alert.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    _is_significant : bool
        :obj:`True` if the event meets the criteria for a signifincat alert.
        :obj:`False` if it does not.

    """
    ev_group = event.get('group', '').lower()
    ev_pipeline = event.get('pipeline', '').lower()
    ev_search = event.get('search', '').lower()
    ev_far = event.get('far', 0.0)
    far_threshold = alert_conditions.get_significant_far(
        ev_group, ev_pipeline, ev_search
    )
    _is_significant = (
        (not event['offline'])
        and ('INJ' not in event['labels'])
        and (ev_far < far_threshold)
    ) or ('RAVEN_ALERT' in event['labels'])

    return _is_significant


def should_publish(event: dict[str, Any]) -> bool:
    """Determine whether an event should be published as a public alert.

    All of the following conditions must be true for a public alert:

    *   The event's ``offline`` flag is not set.
    *   The event's is not an injection.
    *   The event's false alarm rate is less than or equal to
        :obj:`~gwcelery.conf.alert_far_thresholds`

    or the event has been marked to generate a RAVEN alert.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    should_publish : bool
        :obj:`True` if the event meets the criteria for a public alert or
        :obj:`False` if it does not.

    """
    ev_group = event.get('group', '').lower()
    ev_pipeline = event.get('pipeline', '').lower()
    ev_search = event.get('search', '').lower()
    ev_far = event.get('far', 0.0)
    far_threshold = alert_conditions.get_far(ev_group, ev_pipeline, ev_search)
    _should_publish = (
        (not event['offline'])
        and ('INJ' not in event['labels'])
        and (ev_far < far_threshold)
    ) or ('RAVEN_ALERT' in event['labels'])

    return _should_publish


def get_snr(event: dict[str, Any]) -> Any:
    """Get the SNR from the LVAlert packet.

    Different groups and pipelines store the SNR in different fields.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    snr : float
        The SNR.

    """
    group = event.get('group', '').lower()
    pipeline = event.get('pipeline', '').lower()
    if group == 'cbc':
        attribs = event['extra_attributes']['CoincInspiral']
        return attribs['snr']
    elif pipeline == 'cwb':
        attribs = event['extra_attributes']['MultiBurst']
        return attribs['snr']
    elif pipeline == 'olib':
        attribs = event['extra_attributes']['LalInferenceBurst']
        return attribs['omicron_snr_network']
    elif pipeline == 'mly':
        attribs = event['extra_attributes']['MLyBurst']
        return attribs['SNR']
    elif group == 'external':
        return 0.0
    else:
        raise NotImplementedError('SNR attribute not found')


def get_instruments(event: dict[str, Any]) -> Any:
    """Get the instruments that contributed data to an event.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    set
        The set of instruments that contributed to the event.

    """
    attribs = event['extra_attributes']['SingleInspiral']
    ifos = {single['ifo'] for single in attribs}
    return ifos


def get_instruments_in_ranking_statistic(event: dict[str, Any]) -> Any:
    """Get the instruments that contribute to the false alarm rate.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    set
        The set of instruments that contributed to the ranking statistic for
        the event.

    Notes
    -----
    The number of instruments that contributed *data* to an event is given by
    the ``instruments`` key of the GraceDB event JSON structure. However, some
    pipelines (e.g. gstlal) have a distinction between which instruments
    contributed *data* and which were considered in the *ranking* of the
    candidate. For such pipelines, we infer which pipelines contributed to the
    ranking by counting only the SingleInspiral records for which the chi
    squared field is non-empty.

    For PyCBC Live in the O3 configuration, an empty chi^2 field does not mean
    that the detector did not contribute to the ranking; in fact, *all*
    detectors listed in the SingleInspiral table contribute to the significance
    even if the chi^2 is not computed for some of them. Hence PyCBC Live is
    handled as a special case.

    """
    if event['pipeline'].lower() == 'pycbc':
        return set(event['instruments'].split(','))
    else:
        attribs = event['extra_attributes']['SingleInspiral']
        return {single['ifo'] for single in attribs if single.get('chisq') is not None}

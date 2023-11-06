"""Functionality to plot properties of a statistical test
estimated with the package vstats"""
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.interpolate import interp1d


def create_figure_for_rejection_probabilities(
        title: str,
        xaxis_title: str,
        yaxis_title: str,
        xaxis_dtick: Optional[int] = None,
        xaxis_ticklabelstep: int = 1,
        showlegend=False) -> go.Figure:
    """Creates an empty Plotly figure with a layout suitable to
    display rejection probabilities of a statistical test relative
    to the total sample size.

    Parameters
    ----------
    title : str
        Title of the figure.
    xaxis_title : str
        Title of the x-axis of the figure.
    yaxis_title : str
        Title of the y-axis of the figure.
    xaxis_dtick : int, optional
        Distance between ticks on the x-axis. Default None.
    xaxis_ticklabelstep : int
        If this value is set to m, then for every m-th tick
        on the x-axis a label is displayed. Default 1.
    showlegend : bool
        Flag indicating whether a legend should be
        displayed with the plot or not. Default False.

    Returns
    -------
    plotly.graph_objs.Figure
        Empty Plotly figure with a layout suitable to
        display rejection probabilities of a statistical test relative
        to the total sample size.

    Examples
    --------
    >>> from scipy import stats
    >>> import numpy as np
    >>> import vstats
    >>> import vplotly
    >>>
    >>> share_n_group_1 = 0.3
    >>> alpha_test = 0.05
    >>> min_abs_effect = 3  # minimal absolute effect to detect
    >>> sd_1 = 8
    >>> sd_2 = 10
    >>> conf_level_rejection_prob = 0.95
    >>> n_simulation = 10000
    >>>
    >>> est_welchs_test_properties = vstats.get_est_welchs_test_properties(
    >>>     n=[20, 40, 80, 160, 320, 640],
    >>>     share_n_group_1=share_n_group_1,
    >>>     alpha_test=alpha_test,
    >>>     rv_1=stats.norm(loc=min_abs_effect, scale=sd_1),
    >>>     rv_2=stats.norm(loc=0, scale=sd_2),
    >>>     conf_level_rejection_prob=conf_level_rejection_prob,
    >>>     n_simulation=n_simulation,
    >>>     rng=np.random.default_rng(seed=165372562462609342146380204649518102930)
    >>> )
    >>>
    >>> description = (
    >>>     "normal distributions: <br>"
    >>>     "min_abs_effect=" + str(min_abs_effect) + ", "
    >>>     "sd_1=" + str(sd_1) + ", "
    >>>     "sd_2=" + str(sd_2) + ".<br>"
    >>>     "share_n_group_1=" + str(share_n_group_1) + ", "
    >>>     "alpha_test=" + str(alpha_test)
    >>> )
    >>>
    >>> fig = vplotly.create_figure_for_rejection_probabilities(
    >>>     title=("Estimated probabilities for Welch\'s "
    >>>            "test rejecting the null hypothesis"
    >>>            ),
    >>>     xaxis_title="n",
    >>>     yaxis_title="est. rejection probability",
    >>>     showlegend=True
    >>> )
    >>>
    >>> fig = vplotly.add_est_rejection_probabilities_to_figure(
    >>>     fig=fig,
    >>>     est_test_properties=est_welchs_test_properties,
    >>>     color="blue",
    >>>     name=description
    >>> )
    >>>
    >>> fig.show()

    Results of further similar analyses can be added to the figure with
    `vplotly.add_est_rejection_probabilities_to_figure` like above. The figure
    can be manipulated like any Plotly figure. For example the height and
    the width of the plot can be changed with the following command:

    >>> fig.update_layout(height=450, width=950)
    """  # noqa: E501
    layout = go.Layout(
        title=dict(
            text=title,
            pad=dict(b=25),
            yref="paper",
            y=1,
            yanchor="bottom"
        ),
        legend=dict(title="scenario"),
        plot_bgcolor='white',
        xaxis=dict(
            title="n",
            dtick=xaxis_dtick,
            ticklabelstep=xaxis_ticklabelstep,
            gridcolor='lightgrey',
            mirror=True,
            showline=True,
            linecolor='black'
        ),
        yaxis=dict(
            title=yaxis_title,
            dtick=0.05,
            ticklabelstep=2,
            range=[0, 1.04],
            gridcolor='lightgrey',
            mirror=True,
            showline=True,
            linecolor='black'
        ),
        showlegend=showlegend
    )
    fig = go.Figure(layout=layout)
    return (fig)


def add_est_rejection_probabilities_to_figure(
        fig: go.Figure,
        est_test_properties: pd.DataFrame,
        color: str,
        name: Optional[str] = None) -> go.Figure:
    """Adds results of an estimation of rejection probabilities
    of a statistical test as returned by
    `vstats.get_est_welchs_test_properties` to a plotly figure as
    returned by `vplotly.create_figure_for_rejection_probabilities`.
    This means that estimates of the rejection probabilities relative to
    the total sample size are added to the figure together with confidence
    intervals of the true rejection probabilities. In addition this
    function performs a linear interpolation of the estimated rejection
    probabilities and also adds this information to the figure.
    Returns the supplemented figure.

    Parameters
    ----------
    fig : plotly.graph_objs.Figure
        Poltly figure as returned by
        `vplotly.create_figure_for_rejection_probabilities` to add
        the information about the rejection probabilities to.
    est_test_properties : pandas.DataFrame
        Estimated properties of a statistical test
        as generated by `vstats.get_est_welchs_test_properties`. From
        this DataFrame the columns `n`, `rejection_prob_est`,
        `l_conf_int_rejection_prob` and  `ul_conf_int_rejection_prob`
        are used to add information to the figure.
    color : str
        Color with which to add the information about the rejection
        probabilities to the figure.
    name : str, optional
        Legend entry corresponding to the information added to
        the figure. Default None.

    Returns
    -------
    plotly.graph_objs.Figure
        Supplemented figure.

    Examples
    --------
    For an example of the usage see the docstring of
    `vplotly.create_figure_for_rejection_probabilities`.
    """

    # Interpolate at every integer between estimates
    # of the rejection probabilities:
    sp = interp1d(
        x=est_test_properties["n"],
        y=est_test_properties["rejection_prob_est"],
        kind=1  # fit spline of order 1 (linear interpolation)
    )
    n_range = np.arange(
        est_test_properties["n"].iloc[0],
        est_test_properties["n"].iloc[-1] + 1,
        1  # range with step width 1
    )
    # Estimate for reach step in range:
    rejection_prob_est_interpolated = sp(x=n_range)

    trace_0 = go.Scatter(
        x=est_test_properties["n"],
        y=est_test_properties["rejection_prob_est"],
        mode="markers",
        name=name,
        marker=dict(color=color),
        error_y=dict(
            type="data",
            symmetric=False,
            array=(est_test_properties["ul_conf_int_rejection_prob"]
                   - est_test_properties["rejection_prob_est"]
                   ),
            arrayminus=(est_test_properties["rejection_prob_est"]
                        - est_test_properties["ll_conf_int_rejection_prob"]
                        )
        )
    )

    fig.add_trace(trace_0)

    trace_1 = go.Scatter(
        x=n_range,
        y=rejection_prob_est_interpolated,
        mode="lines",
        name="linear interpolation",
        showlegend=False,
        marker=dict(color=trace_0.marker.color)
    )

    fig.add_trace(trace_1)
    return fig

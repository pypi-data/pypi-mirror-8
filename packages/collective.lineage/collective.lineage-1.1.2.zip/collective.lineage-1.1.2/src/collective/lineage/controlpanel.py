from collective.lineage.interfaces import _
from collective.lineage.interfaces import ILineageSettings
from plone.app.registry.browser import controlpanel


class LineageSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ILineageSettings
    label = _(u"Lineage settings")
    description = _(u"""""")

    def updateFields(self):
        super(LineageSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(LineageSettingsEditForm, self).updateWidgets()


class LineageSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = LineageSettingsEditForm

from DateTime import DateTime
from Products.CMFCore.WorkflowCore import WorkflowException
from collective.noticeboard.settings import NoticeboardSettings
from collective.noticeboard.interfaces import INoticeboard
from Products.CMFCore.utils import getToolByName
import logging

logger = logging.getLogger("collective.noticeboard")


def auto_publish(note, event):
    if INoticeboard.providedBy(event.newParent)\
            and getattr(event.newParent, 'layout', '') == 'noticeboardview':
        settings = NoticeboardSettings(event.newParent)
        if settings.publish_on_creation:
            workflowTool = getToolByName(note, "portal_workflow")
            try:
                workflowTool.doActionFor(note, "publish")
            except WorkflowException:
                try:
                    workflowTool.doActionFor(note, "publish_internally")
                except WorkflowException:
                    logger.info("Could not publish:" + str(note.getId()))
                    return
            utils = getToolByName(note, 'plone_utils')
            kwargs = {}
            kwargs['effective_date'] = DateTime()
            utils.contentEdit(note, **kwargs)

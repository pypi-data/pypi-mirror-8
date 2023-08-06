# -*- coding: utf-8 -*-
##########################################################################
#                                                                        #
#        copyright (c) 2010 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################
from Products.CMFCore.utils import getToolByName
from collective.pdfpeek.async import IQueue
from collective.pdfpeek.interfaces import IPDF
from zope.annotation.interfaces import IAnnotations
from zope.component import getSiteManager
from zope.component import getUtility
from zope.component import queryUtility
from zope.component.hooks import setSite
from zope.interface import noLongerProvides

import logging
import transaction

logger = logging.getLogger('collective.pdfpeek.setuphandlers')


def importVarious(context):
    """Miscellanous steps import handle
    """

    if context.readDataFile('collective.pdfpeek_various.txt') is None:
        return


def uninstall(context):
    if context.readDataFile('collective.pdfpeek.uninstall.txt') is None:
        return
    unregisterUtilities(context)
    removePreviewImages(context)
    transaction.commit()


def unregisterUtilities(context):
    portal = context.getSite()
    setSite(portal)
    sm = getSiteManager(portal)
    queue_name = 'collective.pdfpeek.conversion_' + portal.id
    queue = queryUtility(IQueue, queue_name)
    if queue is not None:
        queue_utility = getUtility(IQueue, queue_name)
        sm.unregisterUtility(queue_utility, IQueue)
        del queue_utility
    logger.info('Removed PDFpeek Queue')


def removePreviewImages(context):
    catalog = getToolByName(context.getSite(), 'portal_catalog')
    pdfs = catalog(object_provides=IPDF.__identifier__)
    for pdf in pdfs:
        pdf = pdf.getObject()
        noLongerProvides(pdf, IPDF)
        logger.info('Removed IPDF interface')
        IAnnotations(pdf)
        annotations = IAnnotations(pdf)
        if 'pdfpeek' in annotations:
            del annotations['pdfpeek']
            logger.info('Removed pdf image annotations')

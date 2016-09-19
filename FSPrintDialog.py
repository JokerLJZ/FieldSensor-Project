"""FSPrintDialog create a Print dialog for FSMainWindow.

Copyright (C) 2016 CTTL and TMC.
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).

You could read the sorce code of this programme.
Commercial use was not allowed.
"""
# -*- coding: utf-8 -*-
from BasicUI.PrintDialog import PrintDialog
__author__ = "Joker.Liu"


class FSPrintDialog(PrintDialog):
    """
    FSPrintDialog create a dialog for setting.

    The setting dialog include the configuration option of the test programme.
    """

    def __init__(self):
        """Initial the setting dialog with modal mode."""
        super(FSPrintDialog, self).__init__()

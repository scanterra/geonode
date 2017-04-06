#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import subprocess

from django.conf import settings

log = logging.getLogger(__name__)


def generate_pdf_wkhtml2pdf(url, pdf, map, chart, legend):
    converter_path = settings.RISKS['PDF_GENERATOR']['BIN']
    converter_opts = settings.RISKS['PDF_GENERATOR']['ARGS']
    args = [converter_path] + converter_opts + [url, pdf]
    log.info('running pdf converter with args: %s', args)

    p = subprocess.Popen(' '.join(args), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    stdout, stderr = p.communicate()
    if p.returncode:
        raise ValueError("Cannot generate PDF: {}".format(stderr))
    return pdf



def generate_pdf(url, pdf, map, chart, legend, pdf_gen_name=None):
    pdf_gen_name = pdf_gen_name or settings.RISKS['PDF_GENERATOR']['NAME']
    pdf_gen = globals()['generate_pdf_{}'.format(pdf_gen_name)]

    return pdf_gen(url, pdf, map, chart, legend)


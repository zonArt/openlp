# Copyright 1999-2009 Gentoo Foundation
# Copyright 2010 Jaak Ristioja
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=2
RESTRICT_PYTHON_ABIS="3.*"
inherit python

DESCRIPTION="Free church presentation software"
HOMEPAGE="http://openlp.org/"
SRC_URI="mirror://sourceforge/${PN}/${PV}/OpenLP-${PV}-src.tar.gz"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="alpha amd64 arm hppa ia64 ppc ppc64 sparc x86 x86-fbsd x86-freebsd amd64-linux x86-linux x86-macos x86-solaris"

RDEPEND=">=dev-lang/python-2.5.0
         dev-python/beautifulsoup
         dev-python/chardet
         dev-python/lxml
         dev-python/pyenchant
         dev-python/PyQt4[X,multimedia]
         dev-python/sqlalchemy"
DEPEND="${RDEPEND}"

PYTHON_DEPEND="2:2.5"
PYTHON_MODNAME="openlp"

S=${WORKDIR}/OpenLP-${PV}-src

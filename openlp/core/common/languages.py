# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
The :mod:`languages` module provides a list of language names with utility functions.
"""
from collections import namedtuple

from openlp.core.common import translate


Language = namedtuple('Language', ['id', 'name', 'code'])
languages = sorted([
    Language(1, translate('common.languages', '(Afan) Oromo', 'Language code: om'), 'om'),
    Language(2, translate('common.languages', 'Abkhazian', 'Language code: ab'), 'ab'),
    Language(3, translate('common.languages', 'Afar', 'Language code: aa'), 'aa'),
    Language(4, translate('common.languages', 'Afrikaans', 'Language code: af'), 'af'),
    Language(5, translate('common.languages', 'Albanian', 'Language code: sq'), 'sq'),
    Language(6, translate('common.languages', 'Amharic', 'Language code: am'), 'am'),
    Language(140, translate('common.languages', 'Amuzgo', 'Language code: amu'), 'amu'),
    Language(152, translate('common.languages', 'Ancient Greek', 'Language code: grc'), 'grc'),
    Language(7, translate('common.languages', 'Arabic', 'Language code: ar'), 'ar'),
    Language(8, translate('common.languages', 'Armenian', 'Language code: hy'), 'hy'),
    Language(9, translate('common.languages', 'Assamese', 'Language code: as'), 'as'),
    Language(10, translate('common.languages', 'Aymara', 'Language code: ay'), 'ay'),
    Language(11, translate('common.languages', 'Azerbaijani', 'Language code: az'), 'az'),
    Language(12, translate('common.languages', 'Bashkir', 'Language code: ba'), 'ba'),
    Language(13, translate('common.languages', 'Basque', 'Language code: eu'), 'eu'),
    Language(14, translate('common.languages', 'Bengali', 'Language code: bn'), 'bn'),
    Language(15, translate('common.languages', 'Bhutani', 'Language code: dz'), 'dz'),
    Language(16, translate('common.languages', 'Bihari', 'Language code: bh'), 'bh'),
    Language(17, translate('common.languages', 'Bislama', 'Language code: bi'), 'bi'),
    Language(18, translate('common.languages', 'Breton', 'Language code: br'), 'br'),
    Language(19, translate('common.languages', 'Bulgarian', 'Language code: bg'), 'bg'),
    Language(20, translate('common.languages', 'Burmese', 'Language code: my'), 'my'),
    Language(21, translate('common.languages', 'Byelorussian', 'Language code: be'), 'be'),
    Language(142, translate('common.languages', 'Cakchiquel', 'Language code: cak'), 'cak'),
    Language(22, translate('common.languages', 'Cambodian', 'Language code: km'), 'km'),
    Language(23, translate('common.languages', 'Catalan', 'Language code: ca'), 'ca'),
    Language(24, translate('common.languages', 'Chinese', 'Language code: zh'), 'zh'),
    Language(141, translate('common.languages', 'Comaltepec Chinantec', 'Language code: cco'), 'cco'),
    Language(25, translate('common.languages', 'Corsican', 'Language code: co'), 'co'),
    Language(26, translate('common.languages', 'Croatian', 'Language code: hr'), 'hr'),
    Language(27, translate('common.languages', 'Czech', 'Language code: cs'), 'cs'),
    Language(28, translate('common.languages', 'Danish', 'Language code: da'), 'da'),
    Language(29, translate('common.languages', 'Dutch', 'Language code: nl'), 'nl'),
    Language(30, translate('common.languages', 'English', 'Language code: en'), 'en'),
    Language(31, translate('common.languages', 'Esperanto', 'Language code: eo'), 'eo'),
    Language(32, translate('common.languages', 'Estonian', 'Language code: et'), 'et'),
    Language(33, translate('common.languages', 'Faeroese', 'Language code: fo'), 'fo'),
    Language(34, translate('common.languages', 'Fiji', 'Language code: fj'), 'fj'),
    Language(35, translate('common.languages', 'Finnish', 'Language code: fi'), 'fi'),
    Language(36, translate('common.languages', 'French', 'Language code: fr'), 'fr'),
    Language(37, translate('common.languages', 'Frisian', 'Language code: fy'), 'fy'),
    Language(38, translate('common.languages', 'Galician', 'Language code: gl'), 'gl'),
    Language(39, translate('common.languages', 'Georgian', 'Language code: ka'), 'ka'),
    Language(40, translate('common.languages', 'German', 'Language code: de'), 'de'),
    Language(41, translate('common.languages', 'Greek', 'Language code: el'), 'el'),
    Language(42, translate('common.languages', 'Greenlandic', 'Language code: kl'), 'kl'),
    Language(43, translate('common.languages', 'Guarani', 'Language code: gn'), 'gn'),
    Language(44, translate('common.languages', 'Gujarati', 'Language code: gu'), 'gu'),
    Language(143, translate('common.languages', 'Haitian Creole', 'Language code: ht'), 'ht'),
    Language(45, translate('common.languages', 'Hausa', 'Language code: ha'), 'ha'),
    Language(46, translate('common.languages', 'Hebrew (former iw)', 'Language code: he'), 'he'),
    Language(144, translate('common.languages', 'Hiligaynon', 'Language code: hil'), 'hil'),
    Language(47, translate('common.languages', 'Hindi', 'Language code: hi'), 'hi'),
    Language(48, translate('common.languages', 'Hungarian', 'Language code: hu'), 'hu'),
    Language(49, translate('common.languages', 'Icelandic', 'Language code: is'), 'is'),
    Language(50, translate('common.languages', 'Indonesian (former in)', 'Language code: id'), 'id'),
    Language(51, translate('common.languages', 'Interlingua', 'Language code: ia'), 'ia'),
    Language(52, translate('common.languages', 'Interlingue', 'Language code: ie'), 'ie'),
    Language(54, translate('common.languages', 'Inuktitut (Eskimo)', 'Language code: iu'), 'iu'),
    Language(53, translate('common.languages', 'Inupiak', 'Language code: ik'), 'ik'),
    Language(55, translate('common.languages', 'Irish', 'Language code: ga'), 'ga'),
    Language(56, translate('common.languages', 'Italian', 'Language code: it'), 'it'),
    Language(145, translate('common.languages', 'Jakalteko', 'Language code: jac'), 'jac'),
    Language(57, translate('common.languages', 'Japanese', 'Language code: ja'), 'ja'),
    Language(58, translate('common.languages', 'Javanese', 'Language code: jw'), 'jw'),
    Language(150, translate('common.languages', 'K\'iche\'', 'Language code: quc'), 'quc'),
    Language(59, translate('common.languages', 'Kannada', 'Language code: kn'), 'kn'),
    Language(60, translate('common.languages', 'Kashmiri', 'Language code: ks'), 'ks'),
    Language(61, translate('common.languages', 'Kazakh', 'Language code: kk'), 'kk'),
    Language(146, translate('common.languages', 'Kekchí ', 'Language code: kek'), 'kek'),
    Language(62, translate('common.languages', 'Kinyarwanda', 'Language code: rw'), 'rw'),
    Language(63, translate('common.languages', 'Kirghiz', 'Language code: ky'), 'ky'),
    Language(64, translate('common.languages', 'Kirundi', 'Language code: rn'), 'rn'),
    Language(65, translate('common.languages', 'Korean', 'Language code: ko'), 'ko'),
    Language(66, translate('common.languages', 'Kurdish', 'Language code: ku'), 'ku'),
    Language(67, translate('common.languages', 'Laothian', 'Language code: lo'), 'lo'),
    Language(68, translate('common.languages', 'Latin', 'Language code: la'), 'la'),
    Language(69, translate('common.languages', 'Latvian, Lettish', 'Language code: lv'), 'lv'),
    Language(70, translate('common.languages', 'Lingala', 'Language code: ln'), 'ln'),
    Language(71, translate('common.languages', 'Lithuanian', 'Language code: lt'), 'lt'),
    Language(72, translate('common.languages', 'Macedonian', 'Language code: mk'), 'mk'),
    Language(73, translate('common.languages', 'Malagasy', 'Language code: mg'), 'mg'),
    Language(74, translate('common.languages', 'Malay', 'Language code: ms'), 'ms'),
    Language(75, translate('common.languages', 'Malayalam', 'Language code: ml'), 'ml'),
    Language(76, translate('common.languages', 'Maltese', 'Language code: mt'), 'mt'),
    Language(148, translate('common.languages', 'Mam', 'Language code: mam'), 'mam'),
    Language(77, translate('common.languages', 'Maori', 'Language code: mi'), 'mi'),
    Language(147, translate('common.languages', 'Maori', 'Language code: mri'), 'mri'),
    Language(78, translate('common.languages', 'Marathi', 'Language code: mr'), 'mr'),
    Language(79, translate('common.languages', 'Moldavian', 'Language code: mo'), 'mo'),
    Language(80, translate('common.languages', 'Mongolian', 'Language code: mn'), 'mn'),
    Language(149, translate('common.languages', 'Nahuatl', 'Language code: nah'), 'nah'),
    Language(81, translate('common.languages', 'Nauru', 'Language code: na'), 'na'),
    Language(82, translate('common.languages', 'Nepali', 'Language code: ne'), 'ne'),
    Language(83, translate('common.languages', 'Norwegian', 'Language code: no'), 'no'),
    Language(84, translate('common.languages', 'Occitan', 'Language code: oc'), 'oc'),
    Language(85, translate('common.languages', 'Oriya', 'Language code: or'), 'or'),
    Language(86, translate('common.languages', 'Pashto, Pushto', 'Language code: ps'), 'ps'),
    Language(87, translate('common.languages', 'Persian', 'Language code: fa'), 'fa'),
    Language(151, translate('common.languages', 'Plautdietsch', 'Language code: pdt'), 'pdt'),
    Language(88, translate('common.languages', 'Polish', 'Language code: pl'), 'pl'),
    Language(89, translate('common.languages', 'Portuguese', 'Language code: pt'), 'pt'),
    Language(90, translate('common.languages', 'Punjabi', 'Language code: pa'), 'pa'),
    Language(91, translate('common.languages', 'Quechua', 'Language code: qu'), 'qu'),
    Language(92, translate('common.languages', 'Rhaeto-Romance', 'Language code: rm'), 'rm'),
    Language(93, translate('common.languages', 'Romanian', 'Language code: ro'), 'ro'),
    Language(94, translate('common.languages', 'Russian', 'Language code: ru'), 'ru'),
    Language(95, translate('common.languages', 'Samoan', 'Language code: sm'), 'sm'),
    Language(96, translate('common.languages', 'Sangro', 'Language code: sg'), 'sg'),
    Language(97, translate('common.languages', 'Sanskrit', 'Language code: sa'), 'sa'),
    Language(98, translate('common.languages', 'Scots Gaelic', 'Language code: gd'), 'gd'),
    Language(99, translate('common.languages', 'Serbian', 'Language code: sr'), 'sr'),
    Language(100, translate('common.languages', 'Serbo-Croatian', 'Language code: sh'), 'sh'),
    Language(101, translate('common.languages', 'Sesotho', 'Language code: st'), 'st'),
    Language(102, translate('common.languages', 'Setswana', 'Language code: tn'), 'tn'),
    Language(103, translate('common.languages', 'Shona', 'Language code: sn'), 'sn'),
    Language(104, translate('common.languages', 'Sindhi', 'Language code: sd'), 'sd'),
    Language(105, translate('common.languages', 'Singhalese', 'Language code: si'), 'si'),
    Language(106, translate('common.languages', 'Siswati', 'Language code: ss'), 'ss'),
    Language(107, translate('common.languages', 'Slovak', 'Language code: sk'), 'sk'),
    Language(108, translate('common.languages', 'Slovenian', 'Language code: sl'), 'sl'),
    Language(109, translate('common.languages', 'Somali', 'Language code: so'), 'so'),
    Language(110, translate('common.languages', 'Spanish', 'Language code: es'), 'es'),
    Language(111, translate('common.languages', 'Sudanese', 'Language code: su'), 'su'),
    Language(112, translate('common.languages', 'Swahili', 'Language code: sw'), 'sw'),
    Language(113, translate('common.languages', 'Swedish', 'Language code: sv'), 'sv'),
    Language(114, translate('common.languages', 'Tagalog', 'Language code: tl'), 'tl'),
    Language(115, translate('common.languages', 'Tajik', 'Language code: tg'), 'tg'),
    Language(116, translate('common.languages', 'Tamil', 'Language code: ta'), 'ta'),
    Language(117, translate('common.languages', 'Tatar', 'Language code: tt'), 'tt'),
    Language(118, translate('common.languages', 'Tegulu', 'Language code: te'), 'te'),
    Language(119, translate('common.languages', 'Thai', 'Language code: th'), 'th'),
    Language(120, translate('common.languages', 'Tibetan', 'Language code: bo'), 'bo'),
    Language(121, translate('common.languages', 'Tigrinya', 'Language code: ti'), 'ti'),
    Language(122, translate('common.languages', 'Tonga', 'Language code: to'), 'to'),
    Language(123, translate('common.languages', 'Tsonga', 'Language code: ts'), 'ts'),
    Language(124, translate('common.languages', 'Turkish', 'Language code: tr'), 'tr'),
    Language(125, translate('common.languages', 'Turkmen', 'Language code: tk'), 'tk'),
    Language(126, translate('common.languages', 'Twi', 'Language code: tw'), 'tw'),
    Language(127, translate('common.languages', 'Uigur', 'Language code: ug'), 'ug'),
    Language(128, translate('common.languages', 'Ukrainian', 'Language code: uk'), 'uk'),
    Language(129, translate('common.languages', 'Urdu', 'Language code: ur'), 'ur'),
    Language(153, translate('common.languages', 'Uspanteco', 'Language code: usp'), 'usp'),
    Language(130, translate('common.languages', 'Uzbek', 'Language code: uz'), 'uz'),
    Language(131, translate('common.languages', 'Vietnamese', 'Language code: vi'), 'vi'),
    Language(132, translate('common.languages', 'Volapuk', 'Language code: vo'), 'vo'),
    Language(133, translate('common.languages', 'Welch', 'Language code: cy'), 'cy'),
    Language(134, translate('common.languages', 'Wolof', 'Language code: wo'), 'wo'),
    Language(135, translate('common.languages', 'Xhosa', 'Language code: xh'), 'xh'),
    Language(136, translate('common.languages', 'Yiddish (former ji)', 'Language code: yi'), 'yi'),
    Language(137, translate('common.languages', 'Yoruba', 'Language code: yo'), 'yo'),
    Language(138, translate('common.languages', 'Zhuang', 'Language code: za'), 'za'),
    Language(139, translate('common.languages', 'Zulu', 'Language code: zu'), 'zu')
], key=lambda language: language.name)


def get_language(name):
    """
    Find the language by its name or code.

    :param name: The name or abbreviation of the language.
    :return: The first match as a Language namedtuple or None
    """
    if name:
        name_lower = name.lower()
        name_title = name_lower[:1].upper() + name_lower[1:]
        for language in languages:
            if language.name == name_title or language.code == name_lower:
                return language
    return None

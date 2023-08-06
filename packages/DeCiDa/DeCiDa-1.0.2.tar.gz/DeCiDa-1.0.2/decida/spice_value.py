################################################################################
# FUNCTION : spice_value
# PURPOSE  : return a numeric value, given a "Spice" value
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:30:06 2013
# -----------------------------------------------------------------------------
# NOTES    : 
#
# LICENSE  : (BSD-new)
# 
# This software is provided subject to the following terms and conditions,
# which you should read carefully before using the software.  Using this
# software indicates your acceptance of these terms and conditions.  If you
# do not agree with these terms and conditions, do not use the software.
# 
# Copyright (c) 2013 Richard Booth. All rights reserved.
# 
# Redistribution and use in source or binary forms, with or without
# modifications, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following Disclaimer
#       in each human readable file as well as in the documentation and/or
#       other materials provided with the distribution.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following Disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Richard Booth nor the names of contributors
#       (those who make changes to the software, documentation or other
#       materials) may be used to endorse or promote products derived from
#       this software without specific prior written permission.
# 
# Disclaimer
# 
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, INFRINGEMENT AND THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# ANY USE, MODIFICATION OR DISTRIBUTION OF THIS SOFTWARE IS SOLELY AT THE
# USERS OWN RISK.  IN NO EVENT SHALL RICHARD BOOTH OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, INCLUDING,
# BUT NOT LIMITED TO, CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
# DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
# THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
# IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
# NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
# MODIFICATIONS.
################################################################################
import string
import re
SpiceScale = {
    "t"   : 1e12,
    "g"   : 1e9,
    "meg" : 1e6,
    "k"   : 1e3,
    "m"   : 1e-3,
    "u"   : 1e-6,
    "n"   : 1e-9,
    "p"   : 1e-12,
    "f"   : 1e-15,
    "a"   : 1e-18,
}
def spice_value(val) :
    """ return a numeric value, given a "Spice" value.

    **arguments**:

        .. option:: val (string)

             number in "Spice" format
             (t, g, meg, k, m, u, n, p, f, a are scale factors)

    **results**:

        * return string in normal number format

        * for parameterized values, no change

    **example**:

            >>> import decida
            >>> nums = ["1.23GHz", "1AC", "1FF", "1MEGOHM", "1.2MV", "23KOHM"]
            >>> for num in nums:
            >>>     print num, decida.spice_value(num)
            1.23GHz 1230000000.0
            1AC 1e-18
            1FF 1e-15
            1MEGOHM 1000000.0
            1.2MV 0.0012
            23KOHM 23000.0

    """
    val = string.lower(val)
    m = re.search("^[+]?([0-9]+|[0-9]*\.[0-9]+)(e[+-][0-9]+)?$", val)
    if m :
        return(val)
    m = re.search("^[+]?([0-9]+|[0-9]*\.[0-9]*)(meg|[gkmunpfa])", val)
    if m :
        num = string.atof(m.group(1))
        scl = m.group(2)
        val = num*SpiceScale[scl]
        return(str(val))
    m = re.search("^[+]?([0-9]+|[0-9]*\.[0-9]*)(#inf)", val)
    if m :
        return("1.0")
    #------------------
    # parameter string:
    #------------------
    return(val)

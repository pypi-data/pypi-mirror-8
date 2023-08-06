#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Copyright 2013-2014, Oxidane
All rights reserved

This source has NOT yet been licensed for redistribution, modification, or inclusion in other projects.

An exception has been granted to the official tmuxomatic project, originating from the following addresses:

    https://github.com/oxidane/tmuxomatic
    https://pypi.python.org/pypi/tmuxomatic

A proper open source license is expected to be applied on or before the release of this windowgram module as a separate
project.  Please check this source at a later date for these changes.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

##----------------------------------------------------------------------------------------------------------------------
##
## Windowgram Unit Testing
##
##----------------------------------------------------------------------------------------------------------------------
##
## These tests are ordered; both the test classes and their test methods are run in the order they appear.  This is
## processed automatically using the wrapper class (see code).
##
##      Classes with names starting with "Test", processed in the order they appear
##
##      From these recognized classes, methods with names starting with "test_", processed in the order they appear
##
##----------------------------------------------------------------------------------------------------------------------
##
## Tests are ordered lowest level to highest level:
##
##      Windowgram Convert
##      WindowgramGroup Convert
##      Flex Modifiers
##      Readme Demonstrations
##
## TODO:
##
##      Windowgram
##      Windowgram_Mask
##      PaneList
##
##----------------------------------------------------------------------------------------------------------------------
##
## Notes:
##
##      Hashes should not be used in place of windowgrams, they're needed for comparison in case of failure in testing.
##
##      A change of indentation of the windowgram groups in this source will cause tests to fail because multiline
##      strings are widely used.
##
##----------------------------------------------------------------------------------------------------------------------

import unittest, io, inspect, sys

from windowgram import *



##----------------------------------------------------------------------------------------------------------------------
##
## Keeps the flex modifier unit test producer and validator in sync
##
##----------------------------------------------------------------------------------------------------------------------

FLEXUNIT_MAXWIDTH = 120
FLEXUNIT_INDENT = 12
FLEXUNIT_SPACE = 1



##----------------------------------------------------------------------------------------------------------------------
##
## Unit Testing :: Main
##
##----------------------------------------------------------------------------------------------------------------------

def UnitTests():
    # Sense test classes
    classes = inspect.getmembers(sys.modules[__name__])
    classes = [ classobj for classname, classobj in classes if classname.startswith("Test") ]
    # Pair with line numbers
    classes = [ (classobj, inspect.getsourcelines(classobj)[1]) for classobj in classes ]
    # Sort by line numbers
    classes = sorted(classes, key=lambda tup: tup[1])
    # Run tests in the order they appear
    stream = io.StringIO()
    runner = unittest.TextTestRunner( stream=stream )
    error = ""
    for tup in classes:
        result = runner.run( tup[0]() )
        if not result.wasSuccessful():
            if not error: error = "\n"
            if result.failures: error = error + result.failures[0][1]
            else: error = error + "Unspecified error"
    return error if error else None



##----------------------------------------------------------------------------------------------------------------------
##
## Wrapper class, includes a runTest() that automatically senses tests and executes them
##
##----------------------------------------------------------------------------------------------------------------------

class SenseTestCase(unittest.TestCase):

    def runTest(self):
        # Sense test methods
        methods = inspect.getmembers(self.__class__(), predicate=inspect.ismethod)
        methods = [ method for method in methods if method[0].startswith("test_") ]
        # Pair with line numbers
        methods = [ (method[1], inspect.getsourcelines(method[1])[1]) for method in methods ]
        # Sort by line numbers
        methods = sorted(methods, key=lambda tup: tup[1])
        # Execute tests in the order they appear
        for method in methods: method[0]()

    ##----------------------------------------------------------------------------------------------------------
    ##
    ##  Performs flex commands and compares the resulting windowgrams with those specified
    ##
    ##  Commands        List of strings, each string may have multiple commands but corresponds to one windowgram
    ##  Pattern         Windowgram pattern, where they are ordered left to right, top to bottom, with first line 1-N
    ##
    ##----------------------------------------------------------------------------------------------------------

    def assertFlexSequence(self, commands, pattern):
        windowgramgroup_list = WindowgramGroup_Convert.Pattern_To_List( pattern )
        cmdlen, ptnlen = len(commands), len(windowgramgroup_list)
        if cmdlen != ptnlen:
            raise Exception( "Mismatch: commands (" + str(cmdlen) + ") and windowgrams (" + str(ptnlen) + ")" )
        wg = Windowgram( "1" ) # Specified in case the default changes
        wlist = []
        for ix, (command, windowgram) in enumerate( zip( commands, windowgramgroup_list ) ):
            errors = flex_processor( wg, command )
            self.assertTrue( not errors, errors )
            self.assertTrue( wg.Export_String() == windowgram, 
                "The resulting windowgram for sequence #" + str(ix+1) + " does not match: \n\n" + wg.Export_String() )
            wlist.append( wg.Export_String() )
        pattern_produced = WindowgramGroup_Convert.List_To_Pattern( \
            wlist, FLEXUNIT_MAXWIDTH, FLEXUNIT_INDENT, FLEXUNIT_SPACE )
        pattern_produced = pattern_produced.rstrip(" \t\n").lstrip("\n")
        pattern = pattern.rstrip(" \t\n").lstrip("\n")
        self.assertTrue( pattern_produced == pattern,
            "The resulting pattern does not match specification: \n\n" + pattern_produced + "\n!=\n" + pattern )



##----------------------------------------------------------------------------------------------------------------------
##
## Unit Testing :: Windowgram_Convert
##
##----------------------------------------------------------------------------------------------------------------------

class Test_Windowgram_Convert(SenseTestCase):

    ##----------------------------------------------------------------------------------------------------------
    ##
    ## Windowgram_Convert class
    ##
    ##----------------------------------------------------------------------------------------------------------

    def test_Windowgram_Convert_StringToLines(self):
        data_i = "1135\n1145\n2245\n"
        data_o = [ "1135", "1145", "2245" ]
        data_x = Windowgram_Convert.String_To_Lines( data_i )
        self.assertTrue( data_x == data_o )

    def test_Windowgram_Convert_LinesToString(self):
        data_i = [ "1135", "1145", "2245" ]
        data_o = "1135\n1145\n2245\n"
        data_x = Windowgram_Convert.Lines_To_String( data_i )
        self.assertTrue( data_x == data_o )

    def test_Windowgram_Convert_StringToChars(self):
        data_i = "1135\n1145\n2245\n"
        data_o = [ [ "1", "1", "3", "5" ], [ "1", "1", "4", "5" ], [ "2", "2", "4", "5" ] ]
        data_x = Windowgram_Convert.String_To_Chars( data_i )
        self.assertTrue( data_x == data_o )

    def test_Windowgram_Convert_CharsToString(self):
        data_i = [ [ "1", "1", "3", "5" ], [ "1", "1", "4", "5" ], [ "2", "2", "4", "5" ] ]
        data_o = "1135\n1145\n2245\n"
        data_x = Windowgram_Convert.Chars_To_String( data_i )
        self.assertTrue( data_x == data_o )

    def test_Windowgram_Convert_StringToParsed(self):
        data_i = "1135\n1145\n2245\n"
        data_o = {
            '1': {'y': 1, 'x': 1, 'w': 2, 'n': '1', 'h': 2},
            '2': {'y': 3, 'x': 1, 'w': 2, 'n': '2', 'h': 1},
            '3': {'y': 1, 'x': 3, 'w': 1, 'n': '3', 'h': 1},
            '4': {'y': 2, 'x': 3, 'w': 1, 'n': '4', 'h': 2},
            '5': {'y': 1, 'x': 4, 'w': 1, 'n': '5', 'h': 3}, }
        data_x, error_string, error_line = Windowgram_Convert.String_To_Parsed( data_i )
        self.assertTrue( error_string is None )
        self.assertTrue( error_line is None )
        self.assertTrue( data_x == data_o )

    def test_Windowgram_Convert_ParsedToString(self):
        data_i = {
            '1': {'y': 1, 'x': 1, 'w': 2, 'n': '1', 'h': 2},
            '2': {'y': 3, 'x': 1, 'w': 2, 'n': '2', 'h': 1},
            '3': {'y': 1, 'x': 3, 'w': 1, 'n': '3', 'h': 1},
            '4': {'y': 2, 'x': 3, 'w': 1, 'n': '4', 'h': 2},
            '5': {'y': 1, 'x': 4, 'w': 1, 'n': '5', 'h': 3}, }
        data_o = "1135\n1145\n2245\n"
        data_x = Windowgram_Convert.Parsed_To_String( data_i )
        self.assertTrue( data_x == data_o )

    def test_Windowgram_Convert_StringToMosaic(self):
        data_i = "1135\n1145\n2245\n"
        data_m = [
            "@@::\n@@::\n::::\n",
            "::::\n::::\n@@::\n",
            "::@:\n::::\n::::\n",
            "::::\n::@:\n::@:\n",
            ":::@\n:::@\n:::@\n",
        ]
        data_o = (
            Windowgram("1135\n1145\n2245\n"),
            [
                [ Windowgram("11..\n11..\n....\n"), Windowgram("@@::\n@@::\n::::\n") ],
                [ Windowgram("....\n....\n22..\n"), Windowgram("::::\n::::\n@@::\n") ],
                [ Windowgram("..3.\n....\n....\n"), Windowgram("::@:\n::::\n::::\n") ],
                [ Windowgram("....\n..4.\n..4.\n"), Windowgram("::::\n::@:\n::@:\n") ],
                [ Windowgram("...5\n...5\n...5\n"), Windowgram(":::@\n:::@\n:::@\n") ],
            ],
        )
        data_x = Windowgram_Convert.String_To_Mosaic( data_i, data_m )
        self.assertTrue( Mosaics_Equal( data_x, data_o ) )

    def test_Windowgram_Convert_MosaicToString(self):
        data_i = (
            Windowgram("xxxx\nxxxx\nxxxx\n"), # This will be completely overwritten by the following mask pairs
            [
                [ Windowgram("11..\n11..\n....\n"), Windowgram("@@::\n@@::\n::::\n") ],
                [ Windowgram("....\n....\n22..\n"), Windowgram("::::\n::::\n@@::\n") ],
                [ Windowgram("..3.\n....\n....\n"), Windowgram("::@:\n::::\n::::\n") ],
                [ Windowgram("....\n..4.\n..4.\n"), Windowgram("::::\n::@:\n::@:\n") ],
                [ Windowgram("...5\n...5\n...5\n"), Windowgram(":::@\n:::@\n:::@\n") ],
            ],
        )
        data_o = "1135\n1145\n2245\n"
        data_x = Windowgram_Convert.Mosaic_To_String( data_i )
        self.assertTrue( data_x == data_o )

    def test_Windowgram_Convert_Purify(self):
        data_i = "\n\n1135      \n1145 # etc\n2245\n\n"
        data_o = "1135\n1145\n2245\n"
        data_x = Windowgram_Convert.Purify( data_i )
        self.assertTrue( data_x == data_o )



##----------------------------------------------------------------------------------------------------------------------
##
## Unit Testing :: WindowgramGroup_Convert
##
##----------------------------------------------------------------------------------------------------------------------

class Test_WindowgramGroup_Convert(SenseTestCase):

    def test_WindowgramGroup_Convert_ListToPattern(self):

        # Inclusion of blank lines
        group_i = ['1\n', '2\n2\n']
        group_o = """
            1 2
              2
        """
        group_x = WindowgramGroup_Convert.List_To_Pattern( group_i, 32, 12, 1, testmode=8 )
        self.assertTrue( group_o == group_x )

        # Fitting pattern #1
        group_i = [ '111\n'*3, '2\n'*2, '3333333333\n'*5, 'aaaaaaaaaaaaaaaaa\n'*10, 'bbbbbbbbbbbbbbbbb\n'*5 ]
        group_o = """
            111    2    3333333333
            111    2    3333333333
            111         3333333333
                        3333333333
                        3333333333

            aaaaaaaaaaaaaaaaa    bbbbbbbbbbbbbbbbb
            aaaaaaaaaaaaaaaaa    bbbbbbbbbbbbbbbbb
            aaaaaaaaaaaaaaaaa    bbbbbbbbbbbbbbbbb
            aaaaaaaaaaaaaaaaa    bbbbbbbbbbbbbbbbb
            aaaaaaaaaaaaaaaaa    bbbbbbbbbbbbbbbbb
            aaaaaaaaaaaaaaaaa
            aaaaaaaaaaaaaaaaa
            aaaaaaaaaaaaaaaaa
            aaaaaaaaaaaaaaaaa
            aaaaaaaaaaaaaaaaa
        """
        group_x = WindowgramGroup_Convert.List_To_Pattern( group_i, 50, 12, 4, testmode=8 )
        self.assertTrue( group_o == group_x )

        # Fitting pattern #2
        group_i = [ '111\n'*3, '2\n'*2, '3333333333\n'*5, 'aaaaaaaaaaaaaaaaa\n'*10, 'bbbbbbbbbbbbbbbbb\n'*5 ]
        group_o = """
            111 2 3333333333 aaaaaaaaaaaaaaaaa bbbbbbbbbbbbbbbbb
            111 2 3333333333 aaaaaaaaaaaaaaaaa bbbbbbbbbbbbbbbbb
            111   3333333333 aaaaaaaaaaaaaaaaa bbbbbbbbbbbbbbbbb
                  3333333333 aaaaaaaaaaaaaaaaa bbbbbbbbbbbbbbbbb
                  3333333333 aaaaaaaaaaaaaaaaa bbbbbbbbbbbbbbbbb
                             aaaaaaaaaaaaaaaaa
                             aaaaaaaaaaaaaaaaa
                             aaaaaaaaaaaaaaaaa
                             aaaaaaaaaaaaaaaaa
                             aaaaaaaaaaaaaaaaa
        """
        group_x = WindowgramGroup_Convert.List_To_Pattern( group_i, 100, 12, 1, testmode=8 )
        self.assertTrue( group_o == group_x )

    def test_WindowgramGroup_Convert_PatternToList(self):

        # Test basic height differences
        group_i = """
            1 2
              2
        """
        group_o = ['1\n', '2\n2\n']
        group_x = WindowgramGroup_Convert.Pattern_To_List( group_i )
        self.assertTrue( group_o == group_x )

        # Test special characters like transparency
        group_i = """
            1.. ...
            ... ..2
        """
        group_o = ['1..\n...\n', '...\n..2\n']
        group_x = WindowgramGroup_Convert.Pattern_To_List( group_i )
        self.assertTrue( group_o == group_x )

        # More comprehensive test, including windowgram width mismatch, and '0' as out-of-bounds windowgram
        group_i = """
            1 22 33 aa bb  XX Y ZZ
            1 22    aa bb     Y    0
            1          bb          0
                       bbb
        """
        group_o = ['1\n1\n1\n', '22\n22\n', '33\n', 'aa\naa\n', 'bb\nbb\nbb\nbbb\n', 'XX\n', 'Y\nY\n', 'ZZ\n']
        group_x = WindowgramGroup_Convert.Pattern_To_List( group_i )
        self.assertTrue( group_o == group_x )

        # Test misaligned windowgram lines (second line of second window should be clipped, see expected result)
        group_i = """
            111  222  333
            111   222 333
            111
        """
        group_o = ['111\n111\n111\n', '222\n', '333\n333\n']
        group_x = WindowgramGroup_Convert.Pattern_To_List( group_i )
        self.assertTrue( group_o == group_x )



##----------------------------------------------------------------------------------------------------------------------
##
## Unit Testing :: Flex Modifiers
##
##----------------------------------------------------------------------------------------------------------------------

class Test_FlexModifiers(SenseTestCase):

    ##----------------------------------------------------------------------------------------------------------
    ##
    ## Flex Modifier: Scale
    ##
    ##----------------------------------------------------------------------------------------------------------

    def test_Scale_One_DupCharacters(self): # Created in flex using "new unittest Scale_One_DupCharacters"
        self.assertFlexSequence( [
            "scale 1",
            "scale 19",
            "scale 3",
            "scale 20",
        ], """
            1 1111111111111111111 111 11111111111111111111
              1111111111111111111 111 11111111111111111111
              1111111111111111111 111 11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
              1111111111111111111     11111111111111111111
                                      11111111111111111111
        """ )

    def test_Scale_One_DupPercentages(self): # Created in flex using "new unittest Scale_One_DupPercentages"
        self.assertFlexSequence( [
            "scale 200%",
            "scale 400%",
            "scale 25%",
            "scale 400%",
            "scale 75%",
            "scale 33.4%",
            "scale 100%",
            "scale 100.99%",
            "scale 50%",
            "scale 1000%",
            "scale 050.000%",
        ], """
            11 11111111 11 11111111 111111 11 11 11 1 1111111111 11111
            11 11111111 11 11111111 111111 11 11 11   1111111111 11111
               11111111    11111111 111111            1111111111 11111
               11111111    11111111 111111            1111111111 11111
               11111111    11111111 111111            1111111111 11111
               11111111    11111111 111111            1111111111
               11111111    11111111                   1111111111
               11111111    11111111                   1111111111
                                                      1111111111
                                                      1111111111
        """ )

    def test_Scale_One_DupMultipliers(self): # Created in flex using "new unittest Scale_One_DupMultipliers"
        self.assertFlexSequence( [
            "scale 2x",
            "scale 1x",
            "scale .5x",
            "scale 5x",
            "scale 2.5x",
            "scale 1.25x",
            "scale .2x",
            "scale 5.34x",
            "scale 0.25x",
            "scale 00000.25000x",
        ], """
            11 11 1 11111 111111111111 111111111111111 111 1111111111111111 1111 1
            11 11   11111 111111111111 111111111111111 111 1111111111111111 1111
                    11111 111111111111 111111111111111 111 1111111111111111 1111
                    11111 111111111111 111111111111111     1111111111111111 1111
                    11111 111111111111 111111111111111     1111111111111111
                          111111111111 111111111111111     1111111111111111
                          111111111111 111111111111111     1111111111111111
                          111111111111 111111111111111     1111111111111111
                          111111111111 111111111111111     1111111111111111
                          111111111111 111111111111111     1111111111111111
                          111111111111 111111111111111     1111111111111111
                          111111111111 111111111111111     1111111111111111
                                       111111111111111     1111111111111111
                                       111111111111111     1111111111111111
                                       111111111111111     1111111111111111
                                                           1111111111111111
        """ )

    def test_Scale_One_MixedJoin1(self): # Created in flex using "new unittest Scale_One_MixedJoin1"
        self.assertFlexSequence( [
            "scale 5:10",
            "scale 10:5",
            "scale 2x:2x",
            "scale 50%:50%",
            "scale .5x:5",
            "scale 5:200%",
            "scale 200%:.5x",
        ], """
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111            11111111111111111111                  11111
            11111            11111111111111111111                  11111
            11111            11111111111111111111                  11111
            11111            11111111111111111111                  11111
            11111            11111111111111111111                  11111
        """ )

    def test_Scale_One_MixedJoin2(self): # Created in flex using "new unittest Scale_One_MixedJoin2"
        self.assertFlexSequence( [
            "scale 5x10",
            "scale 10x5",
            "scale 2xx2x",
            "scale 50%x50%",
            "scale .5xx5",
            "scale 5x200%",
            "scale 200%x.5x",
        ], """
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111 1111111111 11111111111111111111 1111111111 11111 11111 1111111111
            11111            11111111111111111111                  11111
            11111            11111111111111111111                  11111
            11111            11111111111111111111                  11111
            11111            11111111111111111111                  11111
            11111            11111111111111111111                  11111
        """ )

    def test_Scale_Two_Mixed(self): # Created in flex using "new unittest Scale_Two_Mixed"
        self.assertFlexSequence( [
            "scale 5 10",
            "scale 10 5",
            "scale 10 2x",
            "scale 2x 200%",
            "scale 50% 10",
            "scale 50% 1.5x",
            "scale 2.5x 10",
            "scale 10 50%",
        ], """
            11111 1111111111 1111111111 11111111111111111111 1111111111 11111 111111111111 1111111111
            11111 1111111111 1111111111 11111111111111111111 1111111111 11111 111111111111 1111111111
            11111 1111111111 1111111111 11111111111111111111 1111111111 11111 111111111111 1111111111
            11111 1111111111 1111111111 11111111111111111111 1111111111 11111 111111111111 1111111111
            11111 1111111111 1111111111 11111111111111111111 1111111111 11111 111111111111 1111111111
            11111            1111111111 11111111111111111111 1111111111 11111 111111111111
            11111            1111111111 11111111111111111111 1111111111 11111 111111111111
            11111            1111111111 11111111111111111111 1111111111 11111 111111111111
            11111            1111111111 11111111111111111111 1111111111 11111 111111111111
            11111            1111111111 11111111111111111111 1111111111 11111 111111111111
                                        11111111111111111111            11111
                                        11111111111111111111            11111
                                        11111111111111111111            11111
                                        11111111111111111111            11111
                                        11111111111111111111            11111
                                        11111111111111111111
                                        11111111111111111111
                                        11111111111111111111
                                        11111111111111111111
                                        11111111111111111111
        """ )

    ##----------------------------------------------------------------------------------------------------------
    ##
    ## Keep this note for adding new unit tests for flex
    ##
    ##   flex> new unittest ScaleCommand    # When created, the output switches to a convenient code dump
    ##   flex> scale 25x10                  # Run commands and the unittest code will be built as you go
    ##   flex> scale 20x20                  # When finished just paste the generated code into this class
    ##
    ##----------------------------------------------------------------------------------------------------------



##----------------------------------------------------------------------------------------------------------------------
##
## Unit Testing :: Readme Demonstrations
##
##----------------------------------------------------------------------------------------------------------------------

class Test_ReadmeDemonstrations(SenseTestCase):

    def test_ReadmeDemonstration1(self): # Created in flex using "new unittest ReadmeDemonstration1"
        self.assertFlexSequence( [
            "scale 25x10",
            "add right 50%",
            "break 0 3x5 A",
            "join ABC.z DG.B EH.L FI.N JM.b KN.l LO.n",
        ], """
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111AAAABBBBCCCC
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111AAAABBBBCCCC
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111DDDDEEEEFFFF
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111DDDDEEEEFFFF
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111GGGGHHHHIIII
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111GGGGHHHHIIII
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111JJJJKKKKLLLL
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111JJJJKKKKLLLL
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111MMMMNNNNOOOO
            1111111111111111111111111 1111111111111111111111111000000000000 1111111111111111111111111MMMMNNNNOOOO

            1111111111111111111111111zzzzzzzzzzzz
            1111111111111111111111111zzzzzzzzzzzz
            1111111111111111111111111BBBBLLLLNNNN
            1111111111111111111111111BBBBLLLLNNNN
            1111111111111111111111111BBBBLLLLNNNN
            1111111111111111111111111BBBBLLLLNNNN
            1111111111111111111111111bbbbllllnnnn
            1111111111111111111111111bbbbllllnnnn
            1111111111111111111111111bbbbllllnnnn
            1111111111111111111111111bbbbllllnnnn
        """ )

    def test_ReadmeDemonstration2(self): # Created in flex using "new unittest ReadmeDemonstration2"
        self.assertFlexSequence( [
            "scale 25x10 ; add right 50% ; break 0 3x5 A ; join ABC.z DG.B EH.L FI.N JM.b KN.l LO.n",
            "split 1 bottom 3 s",
            "rename Nn Dd",
            "swap z s Ll Dd",
        ], """
            1111111111111111111111111zzzzzzzzzzzz 1111111111111111111111111zzzzzzzzzzzz
            1111111111111111111111111zzzzzzzzzzzz 1111111111111111111111111zzzzzzzzzzzz
            1111111111111111111111111BBBBLLLLNNNN 1111111111111111111111111BBBBLLLLNNNN
            1111111111111111111111111BBBBLLLLNNNN 1111111111111111111111111BBBBLLLLNNNN
            1111111111111111111111111BBBBLLLLNNNN 1111111111111111111111111BBBBLLLLNNNN
            1111111111111111111111111BBBBLLLLNNNN 1111111111111111111111111BBBBLLLLNNNN
            1111111111111111111111111bbbbllllnnnn 1111111111111111111111111bbbbllllnnnn
            1111111111111111111111111bbbbllllnnnn sssssssssssssssssssssssssbbbbllllnnnn
            1111111111111111111111111bbbbllllnnnn sssssssssssssssssssssssssbbbbllllnnnn
            1111111111111111111111111bbbbllllnnnn sssssssssssssssssssssssssbbbbllllnnnn

            1111111111111111111111111zzzzzzzzzzzz 1111111111111111111111111ssssssssssss
            1111111111111111111111111zzzzzzzzzzzz 1111111111111111111111111ssssssssssss
            1111111111111111111111111BBBBLLLLDDDD 1111111111111111111111111BBBBDDDDLLLL
            1111111111111111111111111BBBBLLLLDDDD 1111111111111111111111111BBBBDDDDLLLL
            1111111111111111111111111BBBBLLLLDDDD 1111111111111111111111111BBBBDDDDLLLL
            1111111111111111111111111BBBBLLLLDDDD 1111111111111111111111111BBBBDDDDLLLL
            1111111111111111111111111bbbblllldddd 1111111111111111111111111bbbbddddllll
            sssssssssssssssssssssssssbbbblllldddd zzzzzzzzzzzzzzzzzzzzzzzzzbbbbddddllll
            sssssssssssssssssssssssssbbbblllldddd zzzzzzzzzzzzzzzzzzzzzzzzzbbbbddddllll
            sssssssssssssssssssssssssbbbblllldddd zzzzzzzzzzzzzzzzzzzzzzzzzbbbbddddllll
        """ )




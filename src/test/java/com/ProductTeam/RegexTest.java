package com.ProductTeam;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/**
 * RegexTest
 */
public class RegexTest {

    @Test
    public void regexTest()
    {
        String mock_question = App.TEST_QUESTION;
        assertEquals("2311395", RegexHelper.parse_question_id(mock_question));
        assertEquals("Whenever the batterys are low on somebody's remote, why do they just press the buttons even harder?", RegexHelper.parse_question_string(mock_question));
    }

}
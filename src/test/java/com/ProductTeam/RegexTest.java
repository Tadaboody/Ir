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
        String mock_question = "10 who am I?";
        assertEquals(10, RegexHelper.parse_question_id(mock_question));
        assertEquals("who am I?", RegexHelper.parse_question_string(mock_question));
    }

}
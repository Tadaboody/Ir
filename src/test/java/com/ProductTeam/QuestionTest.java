package com.ProductTeam;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.io.IOException;

import org.apache.lucene.document.Document;
import org.junit.Before;
import org.junit.Test;

/**
 * QuestionTest
 */
public class QuestionTest {

    Question question;
    @Before
    public void init() throws IOException
    {
        question = Parser.parse_dataset().get(0);
    }

    @Test
    public void ParsesQuestion() throws IOException
    {
        assertTrue(question.id > 0); // just test that it exists
    }

    @Test
    public void OneRightAnswer()
    {
        int right_answers = 0;
        for(Document answer : question.answerDocuments())
        {
            System.out.println(answer.getField("is_best_answer").stringValue());
            right_answers += (answer.getField("is_best_answer").stringValue() == "true") ? 1 : 0;
        }
        assertEquals(1, right_answers);
    }
}
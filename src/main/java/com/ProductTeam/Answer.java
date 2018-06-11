package com.ProductTeam;

import org.apache.lucene.document.Document;

/**
 * Answer
 */
public class Answer {
    public String answer;
    public float score;
    public static String BODY_FIELD = "answer"; // The name of the main indexable field of an answer
    public Answer(String answer,float score)
    {
        this.answer = answer;
        this.score = score;
    }

    public static Answer fromDocAnswer (Document document,float score)
    {
        return new Answer(document.getField(Answer.BODY_FIELD).stringValue(), score);
    }
}
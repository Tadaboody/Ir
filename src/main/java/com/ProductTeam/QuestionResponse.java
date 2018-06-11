package com.ProductTeam;
/**
 * QuestionResponse
 */

import java.util.List;

public class QuestionResponse {
    public int id;
    public String question;
    public List<Answer> answers;

    public QuestionResponse(int id, List<Answer> answers, String question) {
        this.id = id;
        this.answers = answers;
        this.question = question;
    }
}
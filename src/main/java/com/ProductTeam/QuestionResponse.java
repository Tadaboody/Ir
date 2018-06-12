package com.ProductTeam;
/**
 * QuestionResponse
 */

import java.util.List;

public class QuestionResponse {
    public String id;
    public String question;
    public List<Answer> answers;

    public QuestionResponse(String id, List<Answer> answers, String question) {
        this.id = id;
        this.answers = answers;
        this.question = question;
    }
}
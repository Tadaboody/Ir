package com.ProductTeam;
/**
 * QuestionResponse
 */

import java.util.List;

public class QuestionResponse {
    public int id;
    public List<Answer> answers;

    public QuestionResponse(int id, List<Answer> answers) {
        this.id = id;
        this.answers = answers;
    }
}
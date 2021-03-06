package com.ProductTeam;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.lucene.document.Document;
import org.junit.Before;
import org.junit.Test;

/**
 * QuestionTest
 */
public class QuestionTest{

    private static String[] First_question_nbestanswers = new String[] {
            "A small group of politicians believed strongly that the fact that Saddam Hussien remained in power after the first Gulf War was a signal of weakness to the rest of the world, one that invited attacks and terrorism. Shortly after taking power with George Bush in 2000 and after the attack on 9/11, they were able to use the terrorist attacks to justify war with Iraq on this basis and exaggerated threats of the development of weapons of mass destruction. The military strength of the U.S. and the brutality of Saddam's regime led them to imagine that the military and political victory would be relatively easy.",
            "Because there is a lot of oil in Iraq.",
            "It is tempting to say that the US invaded Iraq because it has lots of oil, but the US is not a country in a deep economic problem that capturing other country\u2019s oil is an actual need for survival. It is more likely that the Iraq invading Kuwait scenario would fall under that assumption.. I think that the US government has come to a conclusion that we are on the verge of a war of religions, or more likely ideologies. It would be presumptuous to try and determent a one cause to the coming war. . I think that the world wide spread of the media with its many forms (Cable, Satellite, Internet, etc.)  have pushed the Moslem regimes to the extreme, fearing that secularity and democratic influence is penetrating their country and will result in an up raising against them. One of the best way to maintain the power that you have and even gain more of it, is by hatred. When the common man is occupied hating an outside enemy, its hatred is kept out side the county and would not be directed towards the regime. . So- I believe that the US understands that the fanatic Moslem regimes have already started a war on the democratic world and now is the time to try a fight it.. . So why invade Iraq? Because it is a huge, week Moslem country that thought to be easy to defeat. . This is exactly the same reason why Afghanistan was first and Syria is next in line.",
            "I think Yuval is pretty spot on. It's a proving ground and a focal point for terror activity that's not on American soil. And, because no one liked Saddam Hussein, no other countries (even in the Middle East) were about to rise up and join his side.. . Rabid speculation: now the Pentagon has a model that says it takes ~5 years, ~$200B and ~2,000 casualties to \"rebuild\" a dictatorship into a democracy. Who's next on the list?" };
    
    private static String First_question_best_answer = "A small group of politicians believed strongly that the fact that Saddam Hussien remained in power after the first Gulf War was a signal of weakness to the rest of the world, one that invited attacks and terrorism. Shortly after taking power with George Bush in 2000 and after the attack on 9/11, they were able to use the terrorist attacks to justify war with Iraq on this basis and exaggerated threats of the development of weapons of mass destruction. The military strength of the U.S. and the brutality of Saddam's regime led them to imagine that the military and political victory would be relatively easy.";
    Question question;

    @Before
    public void init() throws IOException {
        question = Parser.parse_dataset().get(0);
    }

    @Test
    public void ParsesQuestion() throws IOException
    {
        assertEquals("2020338", question.id);
        assertEquals(First_question_best_answer, question.answer);
        assertArrayEquals(First_question_nbestanswers, question.nbestanswers);
    }

    @Test
    public void IndexesAnswers()
    {
        List<String> docAnswers = new ArrayList<>();
        for (Document document : question.answerDocuments()) {
            docAnswers.add(document.getField(Answer.BODY_FIELD).stringValue());
        }
        assertEquals(docAnswers, Arrays.asList(First_question_nbestanswers));
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
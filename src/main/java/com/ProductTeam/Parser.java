package com.ProductTeam;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.util.ArrayList;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;

class Parser
{
    public static List<Question> parse_questions(String path) throws IOException
    {
        Gson gson_parser = new Gson();
        try (Reader fp = new FileReader(path)) {
            JsonReader reader = new JsonReader(fp);
            return gson_parser.fromJson(reader, new ArrayList<Question>().getClass());
        }
    }

    public static void write_answers(String path,List<QuestionResponse> responses) throws IOException
    {
        Gson gson = new GsonBuilder()
        .setPrettyPrinting()
        .disableHtmlEscaping()
        .create();
        try(Writer fp = new FileWriter(path))
        {
            gson.toJson(responses, new ArrayList<QuestionResponse>().getClass(), fp);
        }
    }
}
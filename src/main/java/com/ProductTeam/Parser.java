package com.ProductTeam;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.stream.JsonReader;

class Parser
{
    public List<Question> parse_questions(String path)
    {
        Gson gson_parser = new Gson();
        try (Reader fp = new FileReader(path)) {
            JsonReader reader = new JsonReader(fp);
            return gson_parser.fromJson(reader, new ArrayList<Question>().getClass());
        } catch (IOException ex) {

        }
        return null;

    }
}
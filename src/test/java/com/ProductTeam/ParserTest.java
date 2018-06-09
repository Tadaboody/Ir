package com.ProductTeam;

import static org.junit.Assert.assertTrue;

import java.io.IOException;

import org.junit.Test;

/**
 * ParserTest
 */
public class ParserTest {

    @Test
    public void testReadsDataset() throws IOException
    {
        assertTrue(Parser.parse_dataset().size() > 0);
    }
}
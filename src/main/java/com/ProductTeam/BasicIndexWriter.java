package com.ProductTeam;

import java.io.IOException;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.codecs.lucene70.Lucene70Codec;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.store.Directory;

/**
 * BasicIndexWriter
 */
public class BasicIndexWriter  extends IndexWriter{

    public BasicIndexWriter(Directory dir, Analyzer analyzer) throws IOException
    {
        super(dir, basicConfig(analyzer));
    }
    private static IndexWriterConfig basicConfig(Analyzer analyzer)
    {
        return new IndexWriterConfig(analyzer)
        .setOpenMode(OpenMode.CREATE)
        .setCodec(new Lucene70Codec());
    }
}
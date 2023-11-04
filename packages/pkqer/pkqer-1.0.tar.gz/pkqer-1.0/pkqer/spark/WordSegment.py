package com.xwsoft.nlp

import com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary
import com.hankcs.hanlp.seg.common.Term
import com.hankcs.hanlp.tokenizer.{NLPTokenizer}
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.slf4j.LoggerFactory

import java.util
import scala.collection.{JavaConversions, mutable}

object WordSegment {
  private val logger = LoggerFactory.getLogger(WordSegment.getClass.getSimpleName)

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.WARN)
    //1、解析参数
    logger.warn("job is running please wait for a moment ......")

    //2、获取SparkSession
    val spark: SparkSession = SparkSession.builder().master("local").getOrCreate()
    import spark.implicits._

    val sourceDF = spark
      .sparkContext
      .textFile("file:///C:\\work-space\\idea\\nlp-spark\\data\\text.txt")
      .map(line => {
        val arr = line.split("\t")
        (arr.last)
      }).toDF("context")

    sourceDF.show()
    //5、分词
    val termsDF: DataFrame = sourceDF.mapPartitions(partition => {
      //5.1存放结果的集合
      var resTermList: List[Seq[String]] = List()

      //5.2遍历分区数据
      partition.foreach(row => {
        //5.3获取到字段信息
        val context: String = row.getAs("context").toString

        //5.4分词
        val terms: util.List[Term] = NLPTokenizer.segment(context)
        //5.5去除停用词
        val stopTerms: util.List[Term] = CoreStopWordDictionary.apply(terms) //去除terms中的停用词

        //5.6转换为scala的buffer
        val stopTermsAsScalaBuffer: mutable.Buffer[Term] = JavaConversions.asScalaBuffer(stopTerms)

        //5.7保留名词，去除单个汉字，单词之间使用逗号隔开
        val convertTerms = stopTermsAsScalaBuffer/*.filter(term => {
          term.nature.startsWith("n") && term.word.length != 1
        })*/.map(term => {
          term.word
        })

        //5.8构建单个结果
        var res =  convertTerms

        //5.9去除空值
        if (convertTerms.nonEmpty) {
          resTermList = res :: resTermList //向结果中追加
        }
      })
      resTermList.iterator
    }).toDF( "context_terms")

    termsDF.createOrReplaceTempView("context_terms_table")

    spark.sql(
      """
        |select
        |*
        |from (
        |select
        |term,
        |count(term) as f_count
        |from (
        |select
        |explode(context_terms) as term
        |from context_terms_table
        |)
        |group by term
        |)
        |order by f_count desc
        |""".stripMargin).show()
  }

}

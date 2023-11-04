package nlp

import com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary
import com.hankcs.hanlp.seg.common.Term
import com.hankcs.hanlp.tokenizer.{NLPTokenizer}
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.slf4j.LoggerFactory

import java.util
import scala.collection.{JavaConversions, mutable}

object NetCount3 {

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.WARN)
    //1、解析参数

    //2、获取SparkSession
    val spark: SparkSession = SparkSession.builder().master("local").getOrCreate()

    val sourceDF = spark
      .sparkContext
      .textFile("C:\\Users\\Mi\\Desktop\\spark数据\\spark数据\\reduced.txt")
      .map(_.split("\\s+")).filter(_.length == 6)
      .map(arr => {

        arr(2)
      })
      .map{
        line =>
          line.replace("[","").replace("]","")
      }
      .flatMap{
        line =>
          val terms = NLPTokenizer.segment(line)
          JavaConversions.asScalaBuffer(terms).map(_.word)
      }
      .map((_,1))
      .reduceByKey(_+_)
      .coalesce(1)
      .sortBy(_._2,false)
      .map(_.swap)

    sourceDF.saveAsTextFile("C:\\Users\\Mi\\Desktop\\spark数据\\spark数据\\retrievelog\\output\\key")


  }

}

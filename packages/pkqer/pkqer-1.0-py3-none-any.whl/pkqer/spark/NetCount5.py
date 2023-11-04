package nlp

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession

object NetCount5 {

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.WARN)
    //1、解析参数

    //2、获取SparkSession
    val spark: SparkSession = SparkSession.builder().master("local").getOrCreate()

     val sourceDF = spark
      .sparkContext
       .textFile("C:\\Users\\Mi\\Desktop\\spark数据\\spark数据\\reduced.txt")
       .map(_.split("\\s+")).filter(_.length == 6)
       .cache()
     val num = sourceDF.count()

     val count = sourceDF.map(arr => {
       (arr(3),arr(4))

      })
       .filter(x => x._1 == "1" && x._2 == "1")
       .count()
    val rat = (count * 100.0 / num).formatted("%.2f") + "%"
    val rdd = spark.sparkContext.parallelize(Seq(rat))

    rdd.saveAsTextFile("C:\\Users\\Mi\\Desktop\\spark数据\\spark数据\\retrievelog\\output\\rank\\")


  }

}

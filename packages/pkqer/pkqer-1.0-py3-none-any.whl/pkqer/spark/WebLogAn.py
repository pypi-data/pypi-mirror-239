package nlp

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.sql.types.{BooleanType, StringType, StructField, StructType}

import java.time.format.DateTimeFormatter
import java.util.Locale
import scala.collection.immutable.HashSet

object WebLogAn {

  def formattedDateTime(dateTimeString: String, formattedString: String): String = {
    val src = DateTimeFormatter.ofPattern("dd/MMM/yyyy:HH:mm:ss", Locale.ENGLISH)
    val dst = DateTimeFormatter.ofPattern(formattedString)

    dst.format(src.parse(dateTimeString))
  }

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org.apache").setLevel(Level.ERROR)
    val spark = SparkSession.builder()
      .appName("WebLogAn")
      .master("local[*]")
      .getOrCreate()

    val file = "C:\\Users\\nigaowei\\Desktop\\人工智能训练师\\journal.log"
    val fileRDD = spark.sparkContext.textFile(file).filter(line => line != null && line.trim.split(" ").length > 11)

    /*
    RDD => DataFrame
    1. case class
    2. StructType
     */
    val schema = StructType(Array(
      StructField("requestIP", StringType, false),
      StructField("requestUser", StringType, false),
      StructField("requestTime", StringType, false),
      StructField("requestURL", StringType, false),
      StructField("statusCode", StringType, false),
      StructField("bytesCount", StringType, false),
      StructField("referer", StringType, false),
      StructField("UserAgent", StringType, false),
      StructField("flag", BooleanType, false)
    ))

    // RDD[String] ==> RDD[Row]
    val baseRow = fileRDD.mapPartitions(it => {
      it.map(line => {
        val contents = line.trim.split(" ")
        var flag = true
        if (contents(8).toInt > 400) {
          flag = false
        }
        try {
          Row(
            contents(0),
            contents(1),
            formattedDateTime(contents(3).substring(1), "yyyMMddHH"),
            contents(6),
            contents(8),
            contents(9),
            contents(10),
            if (contents.length > 12) contents(11) + " " + contents(12) else contents(11),
            flag
          )
        } catch {
          case e: Exception => Row("error", "error", "error", "error", "error", "error", "error", false)
        }
      })
    })
    """
      |
      |/about
      |/black-ip-list/
      |/cassandra-clustor/
      |/finance-rhive-repurchase/
      |/hadoop-family-roadmap/
      |/hadoop-hive-intro/
      |/hadoop-zookeeper-intro/
      |/hadoop-mahout-roadmap/
      |""".stripMargin
    val ulrs = HashSet[String]("/about","/black-ip-list/","/cassandra-clustor/","/finance-rhive-repurchase/","/hadoop-family-roadmap/","/hadoop-hive-intro/","/hadoop-zookeeper-intro/","/hadoop-mahout-roadmap/")
    val pvRow = fileRDD.mapPartitions(it => {
      it.map(line => {
        val contents = line.trim.split(" ")
        var flag = true
        if (contents(8).toInt >= 400) {
          flag = false
        } else {
          if (!ulrs.contains(contents(6))) flag = false
        }
        try {
          Row(
            contents(0),
            contents(1),
            formattedDateTime(contents(3).substring(1), "yyyMMddHH"),
            contents(6),
            contents(8),
            contents(9),
            contents(10),
            if (contents.length > 12) contents(11) + " " + contents(12) else contents(11),
            flag
          )
        } catch {
          case e: Exception => Row("error", "error", "error", "error", "error", "error", "error", false)
        }
      })
    })

    val baseDF = spark.createDataFrame(baseRow, schema).filter("flag=true")
    val pvDF = spark.createDataFrame(pvRow, schema).filter("flag=true")

    baseDF.createOrReplaceTempView("base_view")
    pvDF.createOrReplaceTempView("pv_view")

    val parmas = Map(
      "header" -> "false",
      "sep" -> "\t"
    )

    // pv统计
    val pvSQL =
      """
        |select requestURL,count(*) as pv_count from pv_view
        |group by requestURL
        |""".stripMargin
    val pvResult = spark.sql(pvSQL)
    pvResult.coalesce(1).rdd.map{
      row =>
        row(0) + "\t" + row(1)
    }.foreach(println(_))

    // ip
    val ipSQL =
      """
        |select requestIP,count(*) as ip_count from base_view
        |group by requestIP
        |""".stripMargin

    spark.sql(ipSQL).coalesce(1).rdd.map{
              row =>
                row(0) + "\t" + row(1)
            }.foreach(println(_))



    val timeSql =
    """
      |select requestTime,count(*) as ip_count from base_view
      |group by requestTime
      |""".stripMargin
    spark.sql(timeSql).coalesce(1).rdd.map {
      row =>
        row(0) + "\t" + row(1)
    }.foreach(println(_))

    // ua
    val uaSQL =
      """
        |select userAgent,count(*) as ua_count from base_view
        |group by userAgent
        |""".stripMargin

    spark.sql(uaSQL).coalesce(1).rdd.map {
            row =>
              row(0) + "\t" + row(1)
          }.foreach(println(_))




    // stop spark
    spark.stop()
  }

}

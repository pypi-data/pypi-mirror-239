package nlp

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession

object NetCount1 {

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.WARN)
    //1、解析参数

    //2、获取SparkSession
    val spark: SparkSession = SparkSession.builder().master("local").getOrCreate()

    val sourceDF = spark
      .sparkContext
      .textFile("C:\\Users\\Mi\\Desktop\\spark数据\\spark数据\\reduced.txt")
      .map(line => {
        line.split("\\s+")

      })
      .filter(_.length == 6)
      .map {
        line =>
          line.last.split("\\/")(0)
      }
      .filter(_.take(3) == "www")
      .map((_, 1))
      .reduceByKey(_ + _)
      .coalesce(1)
      .sortBy(_._2, false)


    sourceDF.saveAsTextFile("C:\\Users\\Mi\\Desktop\\spark数据\\spark数据\\retrievelog\\output\\url")


  }

}

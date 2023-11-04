package nlp

import com.hankcs.hanlp.tokenizer.NLPTokenizer
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession

import scala.collection.JavaConversions

object NetCount2 {

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.WARN)
    //1、解析参数

    //2、获取SparkSession
    val spark: SparkSession = SparkSession.builder().master("local").getOrCreate()

    val sourceDF = spark
      .sparkContext
      .textFile("C:\\Users\\Mi\\Desktop\\spark数据\\spark数据\\reduced.txt")
      .map(_.split("\\s+")).filter(_.length == 6)
      .map(x =>(x(3), 1))
      .reduceByKey(_ + _)
      .coalesce(1)
      .sortBy(_._2, false)


    sourceDF.saveAsTextFile("C:\\Users\\Mi\\Desktop\\spark数据\\spark数据\\retrievelog\\output\\behavior")


  }

}

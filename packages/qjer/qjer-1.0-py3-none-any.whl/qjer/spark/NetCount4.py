package nlp

import com.hankcs.hanlp.seg.common.Term
import com.hankcs.hanlp.tokenizer.NLPTokenizer
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession
import org.slf4j.LoggerFactory

import java.util
import scala.collection.JavaConversions

object NetCount4 {

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
        val userId = arr(1)
        val searchKey = arr(2).replace("[","").replace("]","")
        (userId + "##" + searchKey,1)
      })
      .reduceByKey(_+_)
      .coalesce(1)
      .sortBy(_._2,false)
      .map{
        case (key,num) =>
          val tmp = key.split("##")
          (tmp(0),tmp(1),num)
      }

    sourceDF.saveAsTextFile("C:\\Users\\Mi\\Desktop\\spark数据\\spark数据\\retrievelog\\output\\userkey\\")

  }

}

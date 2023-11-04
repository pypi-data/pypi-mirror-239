package nlp

import org.apache.hadoop.hbase.{HBaseConfiguration, TableName}
import org.apache.hadoop.hbase.client.{Connection, ConnectionFactory, Put, Table}
import org.apache.hadoop.hbase.util.Bytes
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{ForeachWriter, Row, SparkSession}
import org.apache.spark.sql.functions.get_json_object
import org.apache.spark.sql.streaming.{OutputMode, Trigger}
import org.apache.spark.sql.types.{DoubleType, LongType}

object Analysis {
class HBaseSink(params:Map[String,String]) extends ForeachWriter[Row] {
    private var connection:Connection=_
private var table:Table=_

                        // 连接到HBase
override def open(partitionId: Long, epochId: Long): Boolean = {
    val conf = HBaseConfiguration.create()
conf.set("hbase.zookeeper.quorum",params("hbase.zookeeper.quorum"))
connection = ConnectionFactory.createConnection(conf)
table=connection.getTable(TableName.valueOf(params("hbase.table.name")))
true
}

// 将DataFrame中的数据封装到Put对象
override def process(value: Row): Unit = {
                                         // rowKey=> device_id-device_type
val put = new Put(Bytes.toBytes(value.get(0) + "-" + value.get(1)))

              // 列族：列：value
put.addColumn(
    Bytes.toBytes(params("hbase.column.columnFamily")),
    Bytes.toBytes(params("hbase.column.name")),
    Bytes.toBytes(String.valueOf(value.getAs[Double]("avg_signal")))
)

// 将数据写入HBase
table.put(put)
}

override def close(errorOrNull: Throwable): Unit = {
    table.close()
connection.close()
}
}

def main(args: Array[String]): Unit = {
    Logger.getLogger("org.apache").setLevel(Level.ERROR)
val spark = SparkSession.builder()
.appName("Analysis")
.master("local[*]")
.getOrCreate()

val topic:String="iotTopic"

                 // kafka消费者参数
val kafkaParams = Map(
    "kafka.bootstrap.servers" -> "hadoop000:9092",
                                 "subscribe" -> topic
)

// 连接HBase参数
val hbaseParams = Map(
    "hbase.zookeeper.quorum" -> "hadoop000:2181",
                                "hbase.table.name" -> "spark_iot",
                                                      "hbase.column.columnFamily" -> "info",
                                                                                     "hbase.column.name" -> "avgSignal"
)

val kafkaDF = spark.readStream
              .format("kafka")
              .options(kafkaParams)
              .load()

              // 解析kafka中的消息 jsonString
import spark.implicits._
val df = kafkaDF.selectExpr("cast(value as string)").as[String]
.select(
    get_json_object($"value", "$.deviceID").as("device_id"),
                                              get_json_object($"value", "$.deviceType").as("device_type"),
                                                                                          get_json_object($"value", "$.signal").cast(DoubleType).as("signal"),
                                                                                                                                                   get_json_object($"value", "$.ts").cast(LongType).as("ts")
)

df.createOrReplaceTempView("iot_view")

val sql=
"""
  |select device_id,device_type,round(avg(signal),2) as avg_signal from iot_view
  |group by device_id,device_type
  |""".stripMargin

val result = spark.sql(sql)

             // 写出结果到HBase
result.writeStream
.outputMode(OutputMode.Complete())
.foreach(new HBaseSink(hbaseParams))
.trigger(Trigger.ProcessingTime("5 second"))
.start()
.awaitTermination()

spark.stop()
}

}

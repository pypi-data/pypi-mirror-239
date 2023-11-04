package nlp

import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}
import org.json4s.DefaultFormats
import org.json4s.jackson.Json

import java.util.Properties
import scala.util.Random
case class Message(deviceID:String,deviceType:String,signal:Double,ts:Long)

object UserUtils {
  // 创建Kafka生产者
  def createKafkaProducer(): KafkaProducer[String,String] = {
    val params = new Properties()

    /**
     * Windows:C:/Windows/System32/drivers/etc/hosts
     * macOS:/etc/hosts
     */
    params.setProperty("bootstrap.servers","hadoop000:9092")
    params.setProperty("ack","1")
    params.setProperty("retries","3")
    params.setProperty("key.serializer","org.apache.kafka.common.serialization.StringSerializer")
    params.setProperty("value.serializer","org.apache.kafka.common.serialization.StringSerializer")

    new KafkaProducer[String,String](params)
  }

  def mock(topic:String): Unit = {
    val random = new Random()
    // 模拟设备类型数据
    val deviceTypes = Array("mysql", "redis", "kafka", "route", "spark",
      "flume", "flink", "hadoop")

    // 创建json对象
    val json = new Json(DefaultFormats)

    // 创建生产者对象
    val producer = createKafkaProducer()

    while (true) {
      val index: Int = random.nextInt(deviceTypes.length)
      val deviceID: String = s"device_${random.nextInt(index + 1)}"
      val deviceType = deviceTypes(index)
      val signal = 10 + random.nextInt(90)
      val message = Message(deviceID, deviceType, signal, System.currentTimeMillis())

      // case class object => json string
      val jsonString = json.write(message)
      println(jsonString)

      // 发送消息到kafka指定的topic
      val record = new ProducerRecord[String, String](topic, jsonString)
      producer.send(record)

      Thread.sleep(1000)

    }
  }

}

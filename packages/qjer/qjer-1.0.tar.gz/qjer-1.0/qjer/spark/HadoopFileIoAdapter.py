package com.xwsoft.nlp

import com.hankcs.hanlp.corpus.io.IIOAdapter
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}

import java.io.{InputStream, OutputStream}
import java.net.URI


/**
 * 使用Hanlp必须继承IIOAdapter，因为是使用我们自定义的分词库
 * 当用户自定义语料库在HDFS上的时候，配置此IIOAdapter
 * usage:
 * 1、在HDFS创建/commoon/nlp目录
 * 2、将hanlp.directory.tgz上传到hdfs的目录下
 * 3、在当前工程中配置hanlp.properties
 * 4、在语料库.bin的文件如果存在，加载词典的时候就会直接加载，如果有新词的时候，不会直接加载，
 * 如果有新词的时候，不会直接加载，需要将bin删除，才会
 */
class HadoopFileIoAdapter extends IIOAdapter{

  /**
   * 这个主要是我们需要分词的文件的路径
   * @param s
   * @return
   */
  override def open(path: String): InputStream = {
    //1、获取操作hdfs的文件系统对象
    val configuration = new Configuration()
    val fs: FileSystem = FileSystem.get(URI.create(path), configuration)
    fs.open(new Path(path))
  }

  /**
   * 创建一个文件，用于输出处理后的结果
   * @param s
   * @return
   */
  override def create(path: String): OutputStream = {
    val configuration = new Configuration()
    val fs: FileSystem = FileSystem.get(URI.create(path),configuration)
    fs.create(new Path(path))
  }

}
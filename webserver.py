from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, json, io, urllib, subprocess, os, signal, time, datetime
import _thread
from sys import argv
# The "fake camera feed" input (can be file or URL).
INPUT_PATH = "/home/cache/test.mp4"
# The ffserver configuration file to use.
#CONFIG_PATH = "/home/ndsg/Desktop/thesis/source/fakecam/ffserver.conf"
#LOG_FILE = open("fakecam_"+str(datetime.datetime.now())+".log", "w")

port_number = argv[1]

class S(BaseHTTPRequestHandler):

  def _set_response(self):
      self.send_response(200)
      self.send_header('Content-Type', 'application/octet-stream')
      #self.send_header('Content-Language', 'en')
      self.end_headers()

  def do_GET(self):
      # MAKE OK RESPONSE
      
      ffmpeg_instance = subprocess.Popen(["ffmpeg","-y", "-i",INPUT_PATH,"-f","mp4","-vcodec","libx264","-vf","scale=352:240","-strict","-2","/home/cache/PLEASEWORK"+str(port_number+".mp4")])
      ffmpeg_instance.wait()
      #self._set_response()
      #self.wfile.write(str(str_response).encode('utf-8'))
      self._set_response()
      #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
      # CONTAINS OUTPUT STREAM FOR RESPONSE
      with open("/home/cache/PLEASEWORK"+str(port_number)+".mp4", 'rb') as file: 
        self.wfile.write(file.read())

def run(server_class=HTTPServer, handler_class=S, port=8001):
  logging.basicConfig(level=logging.INFO)
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  logging.info('Starting httpd...\n')
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      pass
  httpd.server_close()
  logging.info('Stopping httpd...\n')

if __name__ == '__main__':
  from sys import argv

  if len(argv) == 2:
      run(port=int(argv[1]))
  else:
      run()
    

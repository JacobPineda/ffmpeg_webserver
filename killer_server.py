from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, json, io, urllib, subprocess, os, signal, time, datetime
import requests
import _thread
from sys import argv
import sys
# The "fake camera feed" input (can be file or URL).
INPUT_PATH = "/home/cache/test.mp4"
# The ffserver configuration file to use.
#CONFIG_PATH = "/home/ndsg/Desktop/thesis/source/fakecam/ffserver.conf"
#LOG_FILE = open("fakecam_"+str(datetime.datetime.now())+".log", "w")

port_pid = dict()
class S(BaseHTTPRequestHandler):

  def _set_response(self):
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.send_header('Content-Language', 'en')
      self.end_headers()

  def do_GET(self):
      # MAKE OK RESPONSE
      query_components = urllib.parse.parse_qs(self.path[2:])
      #print(str(query_components))
      port_num = query_components["port"][0]
      #print(str(port_num))
      #print(port_pid[port_num])
      subprocess.Popen(["kill",str(port_pid[port_num])])
      #os.killpg(int(port_pid[port_num]), signal.SIGTERM)
      self._set_response()
      #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
      # CONTAINS OUTPUT STREAM FOR RESPONSE
      self.wfile.write("ok ok".encode())
  
  def do_POST(self):
      content_length = int(self.headers["Content-Length"])
      post_data = self.rfile.read(content_length)
      new_shit = json.loads(post_data.decode("utf-8"))
      for key, val in new_shit.items():
          port_pid[key] = val
      print(str(port_pid))
      #self._set_response()
      #self.wfile.write("ok ok")
	

def run(server_class=HTTPServer, handler_class=S, port=7777):
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
    

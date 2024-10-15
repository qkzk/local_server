import http.server
import socketserver
import cgi

PORT = 8080  # Le port sur lequel le serveur va écouter


class FileUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Vérification de la longueur du contenu
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            self.send_response(411)  # 411 Length Required
            self.end_headers()
            self.wfile.write(b"Content-Length header is missing.")
            return

        content_length = int(content_length)

        # Lire les données multipart
        ctype, pdict = cgi.parse_header(self.headers.get("Content-Type"))
        print(self.headers)
        if ctype == "multipart/form-data":
            pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
            pdict["CONTENT-LENGTH"] = content_length  # Fixer la longueur

            fields = cgi.parse_multipart(self.rfile, pdict)
            file_data = fields.get("file")[0]  # Récupérer le fichier
            filename = fields.get("filename", ["uploaded_file.txt"])[0]

            # Sauvegarder le fichier sur le serveur
            with open(f"upload/{filename}", "wb") as f:
                f.write(file_data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"File uploaded successfully")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad request: not a multipart/form-data request")


# Serveur HTTP
with socketserver.TCPServer(("", PORT), FileUploadHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

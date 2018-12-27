package main

import (
	"html/template"

	"github.com/go-martini/martini"
	"github.com/martini-contrib/render"
)

func main() {
	m := martini.Classic()
	m.Use(render.Renderer(render.Options{
		Layout:  "layout",
		Charset: "UTF-8",
	}))

	type ServerInfo struct {
		TITLE string
		API   template.URL
	}
	info := ServerInfo{TITLE: "ctas-remote", API: "http://192.168.1.121:12346"}

	m.Get("/", func(r render.Render) {
		r.HTML(200, "controller", info)
	})

	m.RunOnAddr(":12347")
}

//
// go_example_mkv1.go
//

package main
import (
	"fmt"
	"os"

	"github.com/pixelbender/go-matroska/matroska"
	"github.com/quadrifoglio/go-mkv" /* mkv */
)

func main_1() {
	doc, err := matroska.Decode("example.mkv")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(doc.Segment.Info[0].Duration)
}

func main_2() {
	file, err := os.Open("example.mkv"/*"video.webm"*/)
	if err != nil {
		fmt.Fprintf(os.Stderr, "%s\n", err)
		return
	}

	defer file.Close()

	doc := mkv.InitDocument(file)
	err = doc.ParseAll(func(el mkv.Element) {
		fmt.Printf(" Element %s - %d bytes - offset %v\n",
			el.Name, el.Size, doc.GetReadOffset())
	})

	if err != nil {
		fmt.Fprintf(os.Stderr, "%s\n", err)
		return
	}
}

func main() {
	sel := 1
	if len(os.Args) > 1 {
		sel = 2
	}
	switch {
	case sel == 1: main_1()
	case sel == 2: main_2()
	}
}

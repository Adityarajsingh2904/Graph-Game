from django.shortcuts import render
from . import forms
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Node
from neomodel import StructuredNode, StringProperty, BooleanProperty, RelationshipTo, db
from myapp.neo4j_config import ensure_neo4j_connection


# Neomodel Node
class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    friends = RelationshipTo("Person", "KNOWS")
    politician = BooleanProperty()
    cricketer = BooleanProperty()


def index(request):
    return render(request, "index.html")


@csrf_exempt
def collect_all(request):
    if request.method == "POST":
        ensure_neo4j_connection()
        results, meta = db.cypher_query("MATCH (n : Person) RETURN n.name")
        names = [x[0] for x in results]
        return JsonResponse({"alltext": tuple(names)})


@csrf_exempt
def collect_bolly(request):
    if request.method == "POST":
        ensure_neo4j_connection()
        query = "MATCH (n : Person{bollywood:true}) RETURN n.name"
        results, meta = db.cypher_query(query)
        names = [x[0] for x in results]
        return JsonResponse({"alltext": tuple(names)})


@csrf_exempt
def adduser(request):
    if request.method == "POST":
        ensure_neo4j_connection()
        data = json.loads(request.body)
        print(data["value"], data["value2"], data["value3"])
        return HttpResponse(status=200)


@csrf_exempt
def friendrecs(request):
    if request.method == "POST":
        ensure_neo4j_connection()
        data = json.loads(request.body)
        n1 = data["name1"]
        query = (
            f"MATCH (p:Person{{name:'{n1}'}})-[r:KNOWS]-(b)-[:KNOWS]-(friend:Person) "
            f"WHERE NOT EXISTS {{ MATCH (p)-[:KNOWS]-(friend) }} AND (friend.name<>p.name) "
            f"RETURN friend.name, friend.imgLink, count(*) ORDER BY -count(*)"
        )
        results, meta = db.cypher_query(query)
        return JsonResponse({"recos": tuple(results[:10])})
    return render(request, "myapp/index.html")


@csrf_exempt
def collect_mutuals(request):
    if request.method == "POST":
        ensure_neo4j_connection()
        data = json.loads(request.body)
        n1 = data["name1"]
        n2 = data["name2"]
        query = (
            f"MATCH (a:Person {{name:'{n1}'}})-[:KNOWS]-(m)-[:KNOWS]-(c:Person{{name:'{n2}'}}) RETURN m"
        )
        results, meta = db.cypher_query(query)
        mutuals = [[x[0]["name"], x[0]["imgLink"]] for x in results]
        return JsonResponse({"mutuals": tuple(mutuals)})
    return render(request, "myapp/index.html")


@csrf_exempt
def bollymovies(request):
    if request.method == "POST":
        ensure_neo4j_connection()
        data = json.loads(request.body)
        n1 = data["name1"]
        n2 = data["name2"]
        query = (
            f"MATCH (charlie:Person {{name: '{n1}'}}),"
            f"(martin:Person {{name: '{n2}'}}),"
            f"p = shortestPath((charlie)-[*]-(martin)) "
            f"WHERE all(r in relationships(p) WHERE type(r) = 'ACTED_IN') "
            f"RETURN p, NODES(p) as ns"
        )
        results, meta = db.cypher_query(query)
        path = [[node["name"], node["imgLink"]] for node in results[0][1]]
        return JsonResponse({"path": tuple(path)})
    return render(request, "myapp/index.html")


@csrf_exempt
def collect_from_react(request):
    if request.method == "POST":
        ensure_neo4j_connection()
        data = json.loads(request.body)
        n1 = data["name1"]
        n2 = data["name2"]
        query = (
            f"MATCH (b1:Person {{ name:'{n1}' }}), "
            f"(b2:Person{{ name:'{n2}' }}), "
            f"path = shortestPath((b1)-[*..15]-(b2)) RETURN path, NODES(path) as ns;"
        )
        results, meta = db.cypher_query(query)
        path = [[node["name"], node["imgLink"]] for node in results[0][1]]
        return JsonResponse({"shortestpath": tuple(path)})
    return render(request, "myapp/index.html")


@csrf_exempt
def collect_node_given_name(request):
    if request.method == "POST":
        ensure_neo4j_connection()
        data = json.loads(request.body)
        n1 = data["name1"]
        n2 = data["name2"]
        query1 = f"MATCH (b1:Person {{ name:'{n1}' }}) RETURN b1;"
        query2 = f"MATCH (b1:Person {{ name:'{n2}' }}) RETURN b1;"
        results1, _ = db.cypher_query(query1)
        results2, _ = db.cypher_query(query2)
        return JsonResponse({"nodes": (results1[0][0]["imgLink"], results2[0][0]["imgLink"])})
    return render(request, "myapp/index.html")


def form_name_view(request):
    ensure_neo4j_connection()
    form = forms.FormName()
    if request.method == "POST":
        form = forms.FormName(request.POST)
        if form.is_valid():
            form.save(commit=True)
            n1 = form.data["name1"]
            n2 = form.data["name2"]
            query = (
                f"MATCH (b1:Person {{ name:'{n1}' }}), "
                f"(b2:Person{{ name:'{n2}' }}), "
                f"path = shortestPath((b1)-[*..15]-(b2)) RETURN path, NODES(path) as ns;"
            )
            results, _ = db.cypher_query(query)
            names = [node["name"] for node in results[0][1]]
            return render(request, "myapp/shortest.html", {"path": tuple(names)})
    return render(request, "myapp/form_page.html", {"form": form})


def see_nodes(request):
    if request.method == "GET":
        nodes = Node.objects.all()
        return render(request, "myapp/index.html", {"nodes": nodes})
    return render(request, "myapp/index.html")

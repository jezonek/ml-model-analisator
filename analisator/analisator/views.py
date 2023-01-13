from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
import json
from analisator.forms import MLModelForm
from .models import MLModel
import datetime
from django.utils.text import slugify
from .generate_report import generate_report
from reportlab.lib import colors
from reportlab.platypus import (
    Table,
    TableStyle,
    SimpleDocTemplate,
    Paragraph,
)
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER


class ModelsList(generic.ListView):
    model = MLModel
    template_name = "index.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = super(ModelsList, self).get_queryset()

        if self.request.user.is_authenticated:
            queryset = MLModel.objects.order_by("-uploaded_on").filter(
                uploaded_by=self.request.user
            )
        else:
            queryset = []
        return queryset


def ml_model_detail(request, slug):
    template_name = "ml_model_detail.html"
    ml_model = get_object_or_404(MLModel, slug=slug)
    ml_model.report = json.loads(ml_model.report)
    return render(request, template_name, {"ml_model": ml_model})


def upload_files(request):
    if request.method == "POST":
        form = MLModelForm(request.POST, request.FILES)
        if form.is_valid():
            matrix, report = generate_report(
                request.FILES["model_file"], request.FILES["test_file"]
            )
            complete_report = {"matrix": matrix, "report": report}
            instance = MLModel(
                name=form.cleaned_data["name"],
                slug=slugify(form.cleaned_data["name"]),
                uploaded_by=request.user,
                uploaded_on=datetime.datetime.now(),
                report=json.dumps(complete_report),
                model_file=request.FILES["model_file"],
                train_file=request.FILES["train_file"],
                test_file=request.FILES["test_file"],
            )
            instance.save()
            return HttpResponseRedirect("/")
    else:
        form = MLModelForm()
    return render(request, "upload.html", {"form": form})


def convert_report_to_array(report):
    new = []
    new.append(["", "Precision", "Recall", "f1-score", "Support"])

    for row in report:
        if row != "accuracy":
            table_row = [
                row,
                report[row]["precision"],
                report[row]["recall"],
                report[row]["f1score"],
                report[row]["support"],
            ]
        else:
            table_row = [row, report[row], "", "", ""]
        new.append(table_row)
    return new


def generate_pdf(request, slug):
    ml_model = get_object_or_404(MLModel, slug=slug)
    ml_model.report = json.loads(ml_model.report)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename={ml_model.name}.pdf"
    # buffer = BytesIO()
    cm = 2.54
    doc = SimpleDocTemplate(
        response,
        rightMargin=0,
        leftMargin=6.5 * cm,
        topMargin=0.3 * cm,
        bottomMargin=0,
        pagesize=A4,
    )
    elements = []
    ###################################
    style = ParagraphStyle(
        name="Normal",
        fontName="Helvetica",
        fontSize=16,
        spaceAfter=50,
        spaceBefore=30,
        alignment=TA_CENTER,
    )
    elements.append(Paragraph(f"Report for model {ml_model.name}", style=style))
    ###################################
    style = ParagraphStyle(
        name="Normal",
        fontName="Helvetica",
        fontSize=12,
        spaceAfter=12,
        spaceBefore=12,
        alignment=TA_CENTER,
    )
    elements.append(Paragraph("Confusion Matrix", style=style))

    ###################################
    matrix = [
        ["#", 0, 1],
        [0] + ml_model.report["matrix"][0],
        [1] + ml_model.report["matrix"][1],
    ]

    table = Table(matrix, colWidths=30, rowHeights=20)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (4, 0), colors.grey),
                ("ALIGNMENT", (0, 0), (4, 0), "CENTER"),
                ("GRID", (0, 0), (5, 5), 1, colors.black),
                ("VALIGN", (0, 0), (4, 0), "MIDDLE"),
            ]
        )
    )
    elements.append(table)
    elements.append(Paragraph("Classification Report", style=style))

    table = Table(
        convert_report_to_array(ml_model.report["report"]), colWidths=100, rowHeights=30
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (5, 0), colors.grey),
                ("ALIGNMENT", (0, 0), (5, 5), "CENTER"),
                ("GRID", (0, 0), (5, 5), 1, colors.black),
                ("VALIGN", (0, 0), (4, 0), "MIDDLE"),
            ]
        )
    )
    elements.append(table)

    doc.build(elements)

    return response

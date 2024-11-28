from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Profile
from django.views.generic import TemplateView
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io

# Create your views here.


class AcceptView(TemplateView):
    template_name = 'pdf/accept.html'

    def get_context_data(self, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        summary = request.POST.get('summary')
        degree = request.POST.get('degree')
        school = request.POST.get('school')
        university = request.POST.get('university')
        previous_work = request.POST.get('previous_work')
        skills = request.POST.get('skills')

        if name and email and phone:  # Perform basic validation
            profile = Profile.objects.create(
                name=name,
                email=email,
                phone=phone,
                summary=summary,
                degree=degree,
                school=school,
                university=university,
                previous_work=previous_work,
                skills=skills
            )
            return HttpResponseRedirect(f'/cv/{profile.id}/') 

        return self.render_to_response({'error': 'Please fill in all required fields.'})
    


class SuccessView(TemplateView):
    template_name = 'pdf/success.html'


class CVView(TemplateView):
    template_name = 'pdf/cv.html'

    def get(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('id')
        profile = Profile.objects.get(id=profile_id)
        template = loader.get_template(self.template_name)
        html = template.render({'profile': profile})

        config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

        options = {
            'page-size': 'Letter',
            'encoding': 'utf-8',
        }
        pdf = pdfkit.from_string(html, False, options=options, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="cv_{profile.id}.pdf"'
        return response
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.kwargs.get('id')
        context['profile'] = Profile.objects.get(id=profile_id)
        return context
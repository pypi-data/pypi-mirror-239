/*
 * Copyright 2022 Jussi Pakkanen
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <pdfgen.hpp>

using namespace capypdf;

int main(int argc, char **argv) {
    PdfGenerationData opts;

    opts.title = u8string::from_cstr("PDF experiment").value();
    opts.author = u8string::from_cstr("Peter David Foster, esq").value();
    opts.output_colorspace = CAPYPDF_CS_DEVICE_CMYK;
    opts.prof.cmyk_profile_file =
        "/home/jpakkane/Downloads/temp/Adobe ICC Profiles (end-user)/CMYK/UncoatedFOGRA29.icc";

    try {
        GenPopper genpop("test.pdf", opts);
        PdfGen &gen = *genpop.g;
        auto ctxguard = gen.guarded_page_context();
        auto &ctx = ctxguard.ctx;
        {
            ctx.cmd_w(2.0);
            ctx.set_stroke_color(DeviceRGBColor{0.0, 0.3, 1.0});
            ctx.cmd_re(300, 100, 200, 100);
            ctx.cmd_S();
            ctx.render_pdfdoc_text_builtin(
                "This is text in Times New Roman.", CAPY_FONT_TIMES_ROMAN, 12, 100, 500);
            ctx.render_pdfdoc_text_builtin(
                "This is text in Helvetica.", CAPY_FONT_HELVETICA, 12, 100, 480);
            ctx.render_pdfdoc_text_builtin(
                "This is text in Courier.", CAPY_FONT_COURIER, 12, 100, 460);
            ctx.set_nonstroke_color(DeviceRGBColor{1.0, 0.0, 0.9});
            ctx.cmd_re(200, 300, 200, 100);
            ctx.cmd_f();
            const auto sep = gen.create_separation("Gold", DeviceCMYKColor{0, 0.03, 0.55, 0.08});
            ctx.set_color(SeparationColor{sep, 1.0}, false);
            ctx.render_pdfdoc_text_builtin("GOLD!", CAPY_FONT_HELVETICA_BOLD, 32, 250, 340);
        }
        gen.add_page(ctx);
        {
            ctx.cmd_re(100, 300, 200, 100);
            ctx.set_nonstroke_color(DeviceRGBColor{1.0, 0.1, 0.2});
            ctx.cmd_f();
            if(argc > 1) {
                auto image_id = gen.load_image(argv[1]).value();
                auto image_size = gen.get_image_info(image_id);
                auto pop = ctx.push_gstate();
                ctx.cmd_cm(image_size.w / 5, 0, 0, image_size.h / 5, 110, 310);
                ctx.draw_image(image_id);
            }
        }
    } catch(const std::exception &e) {
        printf("ERROR: %s\n", e.what());
        return 1;
    }

    return 0;
}
